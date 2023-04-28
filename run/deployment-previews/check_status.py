#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys
from typing import Callable

import click
import github
from github.GithubException import GithubException
from googleapiclient import discovery
from googleapiclient.errors import HttpError


# cloud run tags much be lowercase
TAG_PREFIX = "pr-"


def make_tag(pr: str) -> str:
    return f"{TAG_PREFIX}{pr}"


def get_pr(tag: str) -> int:
    return int(tag.replace(TAG_PREFIX, ""))


_default_options = [
    click.option(
        "--dry-run",
        help="Dry-run mode. No tag changes made",
        default=False,
        is_flag=True,
    ),
]

_cloudrun_options = [
    click.option("--project-id", required=True, help="Google Cloud Project ID"),
    click.option(
        "--region", required=True, help="Google Cloud Region", default="us-central1"
    ),
    click.option("--service", required=True, help="Google Cloud Run service name"),
]

_github_options = [
    click.option(
        "--repo-name", required=True, help="GitHub repo name (user/repo, or org/repo)"
    )
]


def add_options(options: list[dict]) -> Callable:
    def _add_options(func: Callable) -> Callable:
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def error(msg: str, context: str = None) -> None:
    click.secho(f"Error {context}: ", fg="red", bold=True, nl=False)
    click.echo(msg)
    sys.exit(1)


def get_service(project_id: str, region: str, service_name: str) -> dict:
    """Get the Cloud Run service object"""
    api = discovery.build("run", "v1")
    fqname = f"projects/{project_id}/locations/{region}/services/{service_name}"
    try:
        service = api.projects().locations().services().get(name=fqname).execute()
    except HttpError as e:
        error(re.search('"(.*)"', str(e)).group(0), context="finding service")
    return service


def update_service(project_id: str, region: str, service_name: str, body: dict) -> dict:
    """Update the Cloud Run service."""
    api = discovery.build("run", "v1")
    fqname = f"projects/{project_id}/locations/{region}/services/{service_name}"
    try:
        result = (
            api.projects()
            .locations()
            .services()
            .replaceService(name=fqname, body=body)
            .execute()
        )
    except HttpError as e:
        error(re.search('"(.*)"', str(e)).group(0), context="updating service")
    return result


def get_revision_url(service_obj: dict, tag: str) -> str:
    """Get the revision URL for the tag specified on the service"""
    for revision in service_obj["status"]["traffic"]:
        if revision.get("tag", None) == tag:
            return revision["url"]

    error(
        f"Tag on service {service_obj['metadata']['name']} does not exist.",
        context=f"finding revision tagged {tag}",
    )


def get_revision_tags(service: dict) -> list[str]:
    """Get all tags associated to a service"""
    revs = []

    for revision in service["status"]["traffic"]:
        if revision.get("tag", None):
            revs.append(revision)
    return revs


@click.group()
def cli() -> None:
    """Tool for setting GitHub Status Checks to Cloud Run Revision URLs"""


@cli.command()
@add_options(_default_options)
@add_options(_cloudrun_options)
@add_options(_github_options)
def cleanup(
    dry_run: str, project_id: str, region: str, service: str, repo_name: str
) -> None:
    """Cleanup any revision URLs against closed pull requests"""
    service_obj = get_service(project_id, region, service)
    revs = get_revision_tags(service_obj)

    if not revs:
        click.echo("No revision tags found, nothing to clean up")
        sys.exit(0)

    ghtoken = os.environ.get("GITHUB_TOKEN", None)

    if not ghtoken:
        raise ValueError("GITHUB_TOKEN not defined.")

    try:
        repo = github.Github(ghtoken).get_repo(repo_name)
    except GithubException as e:
        error(e.data["message"], context=f"finding repo {repo_name}")

    tags_to_delete = []

    for rev in revs:
        tag = rev["tag"]
        pr = get_pr(tag)
        pull_request = repo.get_pull(pr)
        if pull_request.state == "closed":
            if dry_run:
                click.secho("Dry-run: ", fg="blue", bold=True, nl=False)
                click.echo(
                    f"PR {pr} is closed, so would remove tag {tag} on service {service}"
                )
            else:
                tags_to_delete.append(tag)

    if tags_to_delete:
        # Edit the service by removing the tags from the traffic spec, then replace the service
        # with this new configuration.
        for tag in tags_to_delete:
            for traffic in service_obj["spec"]["traffic"]:
                if "tag" in traffic.keys() and tag == traffic["tag"]:
                    service_obj["spec"]["traffic"].remove(traffic)

        click.echo(f"Updating the service to remove tags: {','.join(tags_to_delete)}.")
        update_service(project_id, region, service, service_obj)

    else:
        click.echo("Did not identify any tags to delete.")


@cli.command()
@add_options(_default_options)
@add_options(_cloudrun_options)
@add_options(_github_options)
@click.option("--pull-request", required=True, help="GitHub Pull Request ID", type=int)
@click.option("--commit-sha", required=True, help="GitHub commit (SHORT_SHA)")
# [START cloudrun_deployment_preview_setstatus]
def set(
    dry_run: str,
    project_id: str,
    region: str,
    service: str,
    repo_name: str,
    commit_sha: str,
    pull_request: str,
) -> None:
    """Set a status on a GitHub commit to a specific revision URL"""
    service_obj = get_service(project_id, region, service)
    revision_url = get_revision_url(service_obj, tag=make_tag(pull_request))

    ghtoken = os.environ.get("GITHUB_TOKEN", None)

    if not ghtoken:
        raise ValueError("GITHUB_TOKEN not defined.")

    try:
        repo = github.Github(ghtoken).get_repo(repo_name)
    except GithubException as e:
        error(
            e.data["message"],
            context=f"finding repo {repo_name}. Is it a private repo, and does your token have the correct permissions?",
        )

    try:
        commit = repo.get_commit(sha=commit_sha)
    except GithubException as e:
        error(e.data["message"], context=f"finding commit {commit_sha}")

    # [START_EXCLUDE]
    if dry_run:
        click.secho("Dry-run: ", fg="blue", bold=True, nl=False)
        click.echo(
                f"Status would have been created on {repo_name}, "
                f"commit {commit.sha[:7]}, linking to {revision_url} "
                f"on service {service_obj['metadata']['name']}"
        )
        return
    # [END_EXCLUDE]

    commit.create_status(
        state="success",
        target_url=revision_url,
        context=f"Deployment Preview for {service}",
        description="Your preview is now available.",
    )
    click.secho("Success: ", fg="green", bold=True, nl=False)
    click.echo(
        f"Status created on {repo_name}, commit {commit.sha[:7]}, "
        f"linking to {revision_url} on service {service_obj['metadata']['name']}"
    )


# [END cloudrun_deployment_preview_setstatus]

if __name__ == "__main__":
    cli()
