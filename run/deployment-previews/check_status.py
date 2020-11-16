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

import re
import sys
import subprocess

import click
import github
from github.GithubException import GithubException
from google.api_core.exceptions import NotFound
from google.cloud import secretmanager
from googleapiclient import discovery
from googleapiclient.errors import HttpError

TAG_PREFIX = "pr-"


def make_tag(pr):
    return f"{TAG_PREFIX}{pr}"


def get_pr(tag):
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
    ),
    click.option(
        "--ghtoken-secretname",
        default="github_token",
        help="Google Secret Manager secret name",
    ),
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def error(msg, context=None):
    click.secho(f"Error {context}: ", fg="red", bold=True, nl=False)
    click.echo(msg)
    sys.exit(1)


def get_service(project_id, region, service_name):
    """Get the Cloud Run service object"""
    api = discovery.build("run", "v1")
    fqname = f"projects/{project_id}/locations/{region}/services/{service_name}"
    try:
        service = api.projects().locations().services().get(name=fqname).execute()
    except HttpError as e:
        error(re.search('"(.*)"', str(e)).group(0), context="finding service")
    return service


def get_revision_url(service_obj, tag):
    """Get the revision URL for the tag specified on the service"""
    for revision in service_obj["status"]["traffic"]:
        if revision.get("tag", None) == tag:
            return revision["url"]

    error(
        f"Tag on service {service_obj['metadata']['name']} does not exist.",
        context=f"finding revision tagged {tag}",
    )


def get_revision_tags(service):
    """
    Get all tags associated to a service
    """
    revs = []

    for revision in service["status"]["traffic"]:
        if revision.get("tag", None):
            revs.append(revision)
    return revs


def github_token(project_id, ghtoken_secretname):
    """Retrieve GitHub developer token from Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{ghtoken_secretname}/versions/latest"
    try:
        response = client.access_secret_version(name=name)
    except NotFound as e:
        error(e, context=f"finding secret {ghtoken_secretname}")

    github_token = response.payload.data.decode("UTF-8")
    return github_token


@click.group()
def cli():
    """
    Tool for setting GitHub Status Checks to Cloud Run Revision URLs
    """
    pass


@cli.command()
@add_options(_default_options)
@add_options(_cloudrun_options)
@add_options(_github_options)
def cleanup(dry_run, project_id, region, service, repo_name, ghtoken_secretname):
    """
    Cleanup any revision URLs against closed pull requests
    """
    service_obj = get_service(project_id, region, service)
    revs = get_revision_tags(service_obj)

    if not revs:
        click.echo("No revision tags found, nothing to clean up")
        sys.exit(0)

    ghtoken = github_token(project_id, ghtoken_secretname)

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
        tags = ",".join(tags_to_delete)
        # FIX(b/171669848): use discovery API
        # Fork out to the gcloud CLI to programatically delete tags from closed PRs
        click.echo(f"Forking out to gcloud to remove tags: {tags}")
        subprocess.run(
            [
                "gcloud",
                "beta",
                "run",
                "services",
                "update-traffic",
                service,
                "--platform",
                "managed",
                "--region",
                region,
                "--project",
                project_id,
                "--remove-tags",
                tags,
            ],
            check=True,
        )

    else:
        click.echo("Did not identify any tags to delete.")


@cli.command()
@add_options(_default_options)
@add_options(_cloudrun_options)
@add_options(_github_options)
@click.option("--pull-request", required=True, help="GitHub Pull Request ID", type=int)
@click.option("--commit-sha", required=True, help="GitHub commit (SHORT_SHA)")
# [START run_deployment-preview_setstatus]
def set(
    dry_run,
    project_id,
    region,
    service,
    repo_name,
    ghtoken_secretname,
    commit_sha,
    pull_request,
):
    """
    Set a status on a GitHub commit to a specific revision URL
    """
    service_obj = get_service(project_id, region, service)
    revision_url = get_revision_url(service_obj, tag=make_tag(pull_request))

    ghtoken = github_token(project_id, ghtoken_secretname)

    try:
        repo = github.Github(ghtoken).get_repo(repo_name)
    except GithubException as e:
        error(e.data["message"], context=f"finding repo {repo_name}")

    try:
        commit = repo.get_commit(sha=commit_sha)
    except GithubException as e:
        error(e.data["message"], context=f"finding commit {commit_sha}")

    if dry_run:
        click.secho("Dry-run: ", fg="blue", bold=True, nl=False)
        click.echo(
            (
                f"Status would have been created on {repo.repo_name}, "
                f"commit {commit.sha[:7]}, linking to {revision_url} "
                f"on service {service_obj['metadata']['name']}"
            )
        )

    else:
        commit.create_status(
            state="success",
            target_url=revision_url,
            context="Deployment Preview",
            description="Your preview is now available.",
        )
        click.secho("Success: ", fg="green", bold=True, nl=False)
        click.echo(
            f"Status created on {repo.repo_name}, commit {commit.sha[:7]}, "
            f"linking to {revision_url} on service {service_obj['metadata']['name']}"
        )


# [END run_deployment-preview_setstatus]

if __name__ == "__main__":
    cli()
