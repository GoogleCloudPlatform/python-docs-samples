#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database transfer script for Cloud Composer."""

import argparse
import json
import logging
import os
import re
import subprocess
import time
import typing
import uuid

SCRIPT_VERSION = "1.5"

USAGE = r"""This script handles database transfer for Cloud Composer
(Airflow 1.10.14/15 -> Airflow 2.0.1+).

DEPRECATION NOTICE

  This script has been deprecated and will be removed in the future.
  "Snapshots" are recommended tool to perform side-by-side upgrades of
  Cloud Composer environments
  (https://cloud.google.com/composer/docs/save-load-snapshots).

EXPORT

  python3 composer_db_transfer.py export \
    --project [PROJECT NAME] \
    --environment [ENVIRONMENT NAME] \
    --location [REGION] \
    --fernet-key-file [PATH TO FERNET KEY FILE - TO BE CREATED]

  CSV files with exported database are stored as
  /export/tables/[TABLE NAME].csv in the environment's bucket.
  dags, plugins and data directories are stored in
  /export/dirs in the environment's bucket.

  File with a fernet key is going to be created on the machine executing the
  script.

Copying the files between the environments

  Exported files can be copied to the target environment, e.g. with:

  gsutil -m cp -r \
    gs://[SOURCE ENV BUCKET NAME]/export \
    gs://[TARGET ENV BUCKET NAME]/import

IMPORT

  python3 composer_db_transfer.py import \
    --project [PROJECT NAME] \
    --environment [ENVIRONMENT NAME] \
    --location [REGION] \
    --fernet-key-file [PATH TO FERNET KEY FILE FROM SOURCE ENVIRONMENT]

  CSV files that should be imported are expected to be stored as
  /import/tables/[TABLE NAME].csv in the environment's bucket.
  dags, plugins and data directories that should be imported are expected to be
  stored in /import/dirs in the environment's bucket.

  `fernet-key-file` parameter specifies path to the fernet key file of the
  source environment on the machine executing the script. It is created during
  export phase.

  Additional --use-private-gke-endpoint option can be used to access
  environment's GKE cluster through internal endpoint. It might be useful for
  private IP environments.

TROUBLESHOOTING

  Check "Troubleshooting" section of the script manual for troubleshooting
  guidance.

Temporary kubeconfig file is created in the current directory.
"""


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class Command:
    """Provides run_shell_command function to invoke shell commands."""

    class CommandExecutionError(Exception):
        pass

    @staticmethod
    def run_shell_command(
        command: typing.List[str],
        use_shell: bool = False,
        retry_number: int = 3,
        delay: float = 4.0,
        command_input: str = None,
        log_command: bool = True,
        log_error: bool = True,
    ) -> str:
        """Executes shell command with given maximum number of retries on failure."""
        for i in range(retry_number + 1):
            try:
                return Command._run_shell_command(
                    command,
                    use_shell,
                    command_input=command_input,
                    log_command=log_command,
                )
            except Command.CommandExecutionError as e:
                if log_error:
                    logger.error(e)
                if i == retry_number:
                    raise
                time.sleep(delay)
                if log_command:
                    logger.info("Retrying...")

    @staticmethod
    def _run_shell_command(
        command: typing.List[str],
        use_shell: bool = False,
        command_input: str = None,
        log_command: bool = True,
    ) -> str:
        """Executes shell command and returns its output."""

        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell
        )
        if log_command:
            logger.info("Executing shell command: %s", command)
        (res, err) = p.communicate(input=command_input)
        res_string = str(res.decode().strip("\n"))
        if p.returncode:
            logged_command = f' "{command}"' if log_command else ""
            err_string = str(err.decode().strip("\n"))
            error_message = (
                f"Failed to run shell command{logged_command}, "
                f"details:\nstdout = {res_string}\nstderr = {err_string}"
            )
            raise Command.CommandExecutionError(error_message)
        return res_string


class DatabaseUtils:
    """Utility functions for interactions with CloudSQL."""

    # Null values are exported to CSV files as this string. As with high enough
    # probability this string is not going to appear in any value, conversion of
    # nulls to unquoted empty strings (as required by PostgreSQL) can be performed
    # in postprocessing phase with sed.
    null_string = "a8fc0a-b77fe61-a9cf0b-9a0abf"

    @staticmethod
    def nullable(column: str) -> str:
        """Returns SQL expression processing nullable column for export.

        Returned expression transforms nullable column into either its value
        (if not null) or DatabaseUtils.null_string (if null).
        This is necessary to process exported columns as MySQL exports nulls as
        opening double-quote and capital N ("N), wchich breaks CSV file
        structure. Null can not be transformed into empty string here, because
        during import from CSV PostgreSQL differentiates between quoted empty
        string (translated to empty string) and unquoted empty string
        (translated to null).

        Args:
          column: name of the column
        """
        return (
            f'CASE WHEN {column} IS NULL THEN "{DatabaseUtils.null_string}" '
            f"ELSE {column} END"
        )

    @staticmethod
    def nullify(column: str) -> str:
        """Returns a value representing NULL no matter what provided value is."""
        del column
        return f'"{DatabaseUtils.null_string}"'

    @staticmethod
    def blob(column: str) -> str:
        """Returns SQL expression processing blob column for export."""
        big_enough_length_to_hold_hex_representation_of_blob = 150000
        return (
            f'CASE WHEN {column} IS NULL THEN "{DatabaseUtils.null_string}" '
            rf'ELSE CONCAT("\\\x", CAST(HEX({column}) '
            f"as char({big_enough_length_to_hold_hex_representation_of_blob}))) "
            "END"
        )

    @staticmethod
    def fetch_cloudsql_service_account_through_the_workload(
        namespace: str,
        pod_name: str,
        container_name: str,
        sql_instance_name: str,
        project_name: str,
    ) -> str:
        """Returns service account name used by given CloudSQL instance."""
        logger.info("Fetching service account name of Cloud SQL...")
        sql_instance_json = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gcloud sql instances describe {sql_instance_name} "
            f"--project {project_name} --format json",
        )
        sql_instance_config = json.loads(sql_instance_json)
        sql_service_account = sql_instance_config["serviceAccountEmailAddress"]
        logger.info("Cloud SQL service account: %s", sql_service_account)
        return sql_service_account


# List of the tables/columns that should be exported/imported during database
# migration from Airflow 1.10.15 to Airflow 2.*.*.
# (table name, list of columns, does it require fixing sequence number after
# importing explicitly given primary keys)
#
# Order of the tables is relevant as a row can not be inserted if it refers
# (through a foreign key) to not yet inserted row from other table.
#
# dag_code and serialized_dag tables are skipped, as they are going to be
# automatically recreated once DAG code is imported.
tables = [
    ("ab_role", ["id", "name"], True),
    ("ab_permission", ["id", "name"], True),
    (
        "ab_view_menu",
        [
            "id",
            DatabaseUtils.nullable("name"),
        ],
        True,
    ),
    (
        "ab_permission_view",
        [
            "id",
            DatabaseUtils.nullable("permission_id"),
            DatabaseUtils.nullable("view_menu_id"),
        ],
        True,
    ),
    (
        "ab_permission_view_role",
        [
            "id",
            DatabaseUtils.nullable("permission_view_id"),
            DatabaseUtils.nullable("role_id"),
        ],
        True,
    ),
    (
        "ab_register_user",
        [
            "id",
            "first_name",
            "last_name",
            "username",
            DatabaseUtils.nullable("password"),
            "email",
            DatabaseUtils.nullable("registration_date"),
            DatabaseUtils.nullable("registration_hash"),
        ],
        True,
    ),
    (
        "ab_user",
        [
            "id",
            "first_name",
            "last_name",
            "username",
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("active"),
            "email",
            DatabaseUtils.nullable("last_login"),
            DatabaseUtils.nullable("login_count"),
            DatabaseUtils.nullable("fail_login_count"),
            DatabaseUtils.nullable("created_on"),
            DatabaseUtils.nullable("changed_on"),
            DatabaseUtils.nullable("created_by_fk"),
            DatabaseUtils.nullable("changed_by_fk"),
        ],
        True,
    ),
    (
        "ab_user_role",
        [
            "id",
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("role_id"),
        ],
        True,
    ),
    ("alembic_version", ["*"], False),
    (
        "chart",
        [
            "id",
            DatabaseUtils.nullable("label"),
            DatabaseUtils.nullable("conn_id"),
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("chart_type"),
            DatabaseUtils.nullable("sql_layout"),
            DatabaseUtils.nullable("chart.sql"),
            DatabaseUtils.nullable("y_log_scale"),
            DatabaseUtils.nullable("show_datatable"),
            DatabaseUtils.nullable("show_sql"),
            DatabaseUtils.nullable("height"),
            DatabaseUtils.nullable("default_params"),
            DatabaseUtils.nullable("x_is_date"),
            DatabaseUtils.nullable("iteration_no"),
            DatabaseUtils.nullable("last_modified"),
        ],
        True,
    ),
    (
        "connection",
        [
            "id",
            DatabaseUtils.nullable("conn_id"),
            DatabaseUtils.nullable("conn_type"),
            DatabaseUtils.nullable("host"),
            DatabaseUtils.nullable("connection.schema"),
            DatabaseUtils.nullable("login"),
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("port"),
            DatabaseUtils.nullable("extra"),
            DatabaseUtils.nullable("is_encrypted"),
            DatabaseUtils.nullable("is_extra_encrypted"),
        ],
        True,
    ),
    (
        "dag",
        [
            "dag_id",
            DatabaseUtils.nullable("is_paused"),
            DatabaseUtils.nullable("is_subdag"),
            DatabaseUtils.nullable("is_active"),
            DatabaseUtils.nullable("last_scheduler_run"),
            DatabaseUtils.nullable("last_pickled"),
            DatabaseUtils.nullable("last_expired"),
            DatabaseUtils.nullable("scheduler_lock"),
            DatabaseUtils.nullable("pickle_id"),
            DatabaseUtils.nullable("fileloc"),
            DatabaseUtils.nullable("owners"),
            # Description might be a multi-line string.
            # PostgreSQL is not able to consume CSV files with rows containing
            # multi-line strings in a form produced by MySQL. Some
            # post-processing might be a possible solution, but introducing
            # additional complexity is not justified as the description is
            # going to be re-created anyways once a DAG is parsed in a target
            # environment.
            DatabaseUtils.nullify("description"),
            DatabaseUtils.nullable("default_view"),
            DatabaseUtils.nullable("schedule_interval"),
            DatabaseUtils.nullable("root_dag_id"),
        ],
        False,
    ),
    (
        "dag_pickle",
        [
            "id",
            DatabaseUtils.blob("pickle"),
            DatabaseUtils.nullable("created_dttm"),
            DatabaseUtils.nullable("pickle_hash"),
        ],
        True,
    ),
    (
        "dag_run",
        [
            "id",
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("execution_date"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("run_id"),
            DatabaseUtils.nullable("external_trigger"),
            DatabaseUtils.blob("conf"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("start_date"),
        ],
        True,
    ),
    ("dag_tag", ["*"], False),
    (
        "import_error",
        [
            "id",
            DatabaseUtils.nullable("timestamp"),
            DatabaseUtils.nullable("filename"),
            DatabaseUtils.nullable("stacktrace"),
        ],
        True,
    ),
    (
        "job",
        [
            "id",
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("job_type"),
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("latest_heartbeat"),
            DatabaseUtils.nullable("executor_class"),
            DatabaseUtils.nullable("hostname"),
            DatabaseUtils.nullable("unixname"),
        ],
        True,
    ),
    (
        "known_event",
        [
            "id",
            DatabaseUtils.nullable("label"),
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("user_id"),
            DatabaseUtils.nullable("known_event_type_id"),
            DatabaseUtils.nullable("description"),
        ],
        True,
    ),
    (
        "known_event_type",
        [
            "id",
            DatabaseUtils.nullable("know_event_type"),
        ],
        True,
    ),
    (
        "kube_resource_version",
        [
            "one_row_id",
            DatabaseUtils.nullable("resource_version"),
        ],
        False,
    ),
    (
        "kube_worker_uuid",
        [
            "one_row_id",
            DatabaseUtils.nullable("worker_uuid"),
        ],
        False,
    ),
    (
        "log",
        [
            "id",
            DatabaseUtils.nullable("dttm"),
            DatabaseUtils.nullable("dag_id"),
            DatabaseUtils.nullable("task_id"),
            DatabaseUtils.nullable("event"),
            DatabaseUtils.nullable("execution_date"),
            DatabaseUtils.nullable("owner"),
            DatabaseUtils.nullable("extra"),
        ],
        True,
    ),
    ("rendered_task_instance_fields", ["*"], False),
    (
        "sla_miss",
        [
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("email_sent"),
            DatabaseUtils.nullable("timestamp"),
            DatabaseUtils.nullable("description"),
            DatabaseUtils.nullable("notification_sent"),
        ],
        False,
    ),
    (
        "slot_pool",
        [
            "id",
            DatabaseUtils.nullable("pool"),
            DatabaseUtils.nullable("slots"),
            DatabaseUtils.nullable("description"),
        ],
        True,
    ),
    (
        "task_fail",
        [
            "id",
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("duration"),
        ],
        True,
    ),
    (
        "task_instance",
        [
            "task_id",
            "dag_id",
            "execution_date",
            DatabaseUtils.nullable("start_date"),
            DatabaseUtils.nullable("end_date"),
            DatabaseUtils.nullable("duration"),
            DatabaseUtils.nullable("state"),
            DatabaseUtils.nullable("try_number"),
            DatabaseUtils.nullable("hostname"),
            DatabaseUtils.nullable("unixname"),
            DatabaseUtils.nullable("job_id"),
            "pool",
            DatabaseUtils.nullable("queue"),
            DatabaseUtils.nullable("priority_weight"),
            DatabaseUtils.nullable("operator"),
            DatabaseUtils.nullable("queued_dttm"),
            DatabaseUtils.nullable("pid"),
            DatabaseUtils.nullable("max_tries"),
            DatabaseUtils.blob("executor_config"),
            DatabaseUtils.nullable("pool_slots"),
        ],
        False,
    ),
    (
        "task_reschedule",
        [
            "id",
            "task_id",
            "dag_id",
            "execution_date",
            "try_number",
            "start_date",
            "end_date",
            "duration",
            "reschedule_date",
        ],
        True,
    ),
    (
        "users",
        [
            "id",
            DatabaseUtils.nullable("username"),
            DatabaseUtils.nullable("email"),
            DatabaseUtils.nullable("password"),
            DatabaseUtils.nullable("superuser"),
        ],
        True,
    ),
    (
        "variable",
        [
            "id",
            DatabaseUtils.nullable("variable.key"),
            DatabaseUtils.nullable("val"),
            DatabaseUtils.nullable("is_encrypted"),
        ],
        True,
    ),
    (
        "xcom",
        [
            "id",
            DatabaseUtils.nullable("xcom.key"),
            DatabaseUtils.blob("value"),
            "timestamp",
            "execution_date",
            "task_id",
            "dag_id",
        ],
        True,
    ),
]


sql_dump_of_empty_airflow_1_10_14_database_for_postgres_13 = r"""
--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ab_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_permission (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


--
-- Name: ab_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_permission_id_seq OWNED BY public.ab_permission.id;


--
-- Name: ab_permission_view; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_permission_view (
    id integer NOT NULL,
    permission_id integer,
    view_menu_id integer
);


--
-- Name: ab_permission_view_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_permission_view_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_permission_view_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_permission_view_id_seq OWNED BY public.ab_permission_view.id;


--
-- Name: ab_permission_view_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_permission_view_role (
    id integer NOT NULL,
    permission_view_id integer,
    role_id integer
);


--
-- Name: ab_permission_view_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_permission_view_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_permission_view_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_permission_view_role_id_seq OWNED BY public.ab_permission_view_role.id;


--
-- Name: ab_register_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_register_user (
    id integer NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(256),
    email character varying(64) NOT NULL,
    registration_date timestamp without time zone,
    registration_hash character varying(256)
);


--
-- Name: ab_register_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_register_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_register_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_register_user_id_seq OWNED BY public.ab_register_user.id;


--
-- Name: ab_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_role (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


--
-- Name: ab_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_role_id_seq OWNED BY public.ab_role.id;


--
-- Name: ab_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_user (
    id integer NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(256),
    active boolean,
    email character varying(64) NOT NULL,
    last_login timestamp without time zone,
    login_count integer,
    fail_login_count integer,
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    created_by_fk integer,
    changed_by_fk integer
);


--
-- Name: ab_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_user_id_seq OWNED BY public.ab_user.id;


--
-- Name: ab_user_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_user_role (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


--
-- Name: ab_user_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_user_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_user_role_id_seq OWNED BY public.ab_user_role.id;


--
-- Name: ab_view_menu; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ab_view_menu (
    id integer NOT NULL,
    name character varying(250) NOT NULL
);


--
-- Name: ab_view_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ab_view_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ab_view_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ab_view_menu_id_seq OWNED BY public.ab_view_menu.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: chart; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chart (
    id integer NOT NULL,
    label character varying(200),
    conn_id character varying(250) NOT NULL,
    user_id integer,
    chart_type character varying(100),
    sql_layout character varying(50),
    sql text,
    y_log_scale boolean,
    show_datatable boolean,
    show_sql boolean,
    height integer,
    default_params character varying(5000),
    x_is_date boolean,
    iteration_no integer,
    last_modified timestamp with time zone
);


--
-- Name: chart_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chart_id_seq OWNED BY public.chart.id;


--
-- Name: connection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.connection (
    id integer NOT NULL,
    conn_id character varying(250),
    conn_type character varying(500),
    host character varying(100),
    schema character varying(500),
    login character varying(500),
    password character varying(5000),
    port integer,
    extra character varying(5000),
    is_encrypted boolean,
    is_extra_encrypted boolean
);


--
-- Name: connection_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.connection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: connection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.connection_id_seq OWNED BY public.connection.id;


--
-- Name: dag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dag (
    dag_id character varying(250) NOT NULL,
    is_paused boolean,
    is_subdag boolean,
    is_active boolean,
    last_scheduler_run timestamp with time zone,
    last_pickled timestamp with time zone,
    last_expired timestamp with time zone,
    scheduler_lock boolean,
    pickle_id integer,
    fileloc character varying(2000),
    owners character varying(2000),
    description text,
    default_view character varying(25),
    schedule_interval text,
    root_dag_id character varying(250)
);


--
-- Name: dag_code; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dag_code (
    fileloc_hash bigint NOT NULL,
    fileloc character varying(2000) NOT NULL,
    source_code text NOT NULL,
    last_updated timestamp with time zone NOT NULL
);


--
-- Name: dag_pickle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dag_pickle (
    id integer NOT NULL,
    pickle bytea,
    created_dttm timestamp with time zone,
    pickle_hash bigint
);


--
-- Name: dag_pickle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dag_pickle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dag_pickle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dag_pickle_id_seq OWNED BY public.dag_pickle.id;


--
-- Name: dag_run; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dag_run (
    id integer NOT NULL,
    dag_id character varying(250),
    execution_date timestamp with time zone,
    state character varying(50),
    run_id character varying(250),
    external_trigger boolean,
    conf bytea,
    end_date timestamp with time zone,
    start_date timestamp with time zone
);


--
-- Name: dag_run_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dag_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dag_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dag_run_id_seq OWNED BY public.dag_run.id;


--
-- Name: dag_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dag_tag (
    name character varying(100) NOT NULL,
    dag_id character varying(250) NOT NULL
);


--
-- Name: import_error; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.import_error (
    id integer NOT NULL,
    "timestamp" timestamp with time zone,
    filename character varying(1024),
    stacktrace text
);


--
-- Name: import_error_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.import_error_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: import_error_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.import_error_id_seq OWNED BY public.import_error.id;


--
-- Name: job; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job (
    id integer NOT NULL,
    dag_id character varying(250),
    state character varying(20),
    job_type character varying(30),
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    latest_heartbeat timestamp with time zone,
    executor_class character varying(500),
    hostname character varying(100),
    unixname character varying(1000)
);


--
-- Name: job_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.job_id_seq OWNED BY public.job.id;


--
-- Name: known_event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.known_event (
    id integer NOT NULL,
    label character varying(200),
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    user_id integer,
    known_event_type_id integer,
    description text
);


--
-- Name: known_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.known_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: known_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.known_event_id_seq OWNED BY public.known_event.id;


--
-- Name: known_event_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.known_event_type (
    id integer NOT NULL,
    know_event_type character varying(200)
);


--
-- Name: known_event_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.known_event_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: known_event_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.known_event_type_id_seq OWNED BY public.known_event_type.id;


--
-- Name: kube_resource_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kube_resource_version (
    one_row_id boolean DEFAULT true NOT NULL,
    resource_version character varying(255),
    CONSTRAINT kube_resource_version_one_row_id CHECK (one_row_id)
);


--
-- Name: kube_worker_uuid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kube_worker_uuid (
    one_row_id boolean DEFAULT true NOT NULL,
    worker_uuid character varying(255),
    CONSTRAINT kube_worker_one_row_id CHECK (one_row_id)
);


--
-- Name: log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.log (
    id integer NOT NULL,
    dttm timestamp with time zone,
    dag_id character varying(250),
    task_id character varying(250),
    event character varying(30),
    execution_date timestamp with time zone,
    owner character varying(500),
    extra text
);


--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.log_id_seq OWNED BY public.log.id;


--
-- Name: rendered_task_instance_fields; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rendered_task_instance_fields (
    dag_id character varying(250) NOT NULL,
    task_id character varying(250) NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    rendered_fields json NOT NULL
);


--
-- Name: serialized_dag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.serialized_dag (
    dag_id character varying(250) NOT NULL,
    fileloc character varying(2000) NOT NULL,
    fileloc_hash bigint NOT NULL,
    data json NOT NULL,
    last_updated timestamp with time zone NOT NULL,
    dag_hash character varying(32) DEFAULT 'Hash not calculated yet'::character varying NOT NULL
);


--
-- Name: sla_miss; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sla_miss (
    task_id character varying(250) NOT NULL,
    dag_id character varying(250) NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    email_sent boolean,
    "timestamp" timestamp with time zone,
    description text,
    notification_sent boolean
);


--
-- Name: slot_pool; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.slot_pool (
    id integer NOT NULL,
    pool character varying(50),
    slots integer,
    description text
);


--
-- Name: slot_pool_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.slot_pool_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: slot_pool_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.slot_pool_id_seq OWNED BY public.slot_pool.id;


--
-- Name: task_fail; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_fail (
    id integer NOT NULL,
    task_id character varying(250) NOT NULL,
    dag_id character varying(250) NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    duration integer
);


--
-- Name: task_fail_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.task_fail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: task_fail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.task_fail_id_seq OWNED BY public.task_fail.id;


--
-- Name: task_instance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_instance (
    task_id character varying(250) NOT NULL,
    dag_id character varying(250) NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    duration double precision,
    state character varying(20),
    try_number integer,
    hostname character varying(100),
    unixname character varying(1000),
    job_id integer,
    pool character varying(50) NOT NULL,
    queue character varying(256),
    priority_weight integer,
    operator character varying(1000),
    queued_dttm timestamp with time zone,
    pid integer,
    max_tries integer DEFAULT '-1'::integer,
    executor_config bytea,
    pool_slots integer
);


--
-- Name: task_reschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_reschedule (
    id integer NOT NULL,
    task_id character varying(250) NOT NULL,
    dag_id character varying(250) NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    try_number integer NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    reschedule_date timestamp with time zone NOT NULL
);


--
-- Name: task_reschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.task_reschedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: task_reschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.task_reschedule_id_seq OWNED BY public.task_reschedule.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(250),
    email character varying(500),
    password character varying(255),
    superuser boolean
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_seq OWNED BY public.users.id;


--
-- Name: variable; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.variable (
    id integer NOT NULL,
    key character varying(250),
    val text,
    is_encrypted boolean
);


--
-- Name: variable_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.variable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.variable_id_seq OWNED BY public.variable.id;


--
-- Name: xcom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.xcom (
    id integer NOT NULL,
    key character varying(512),
    value bytea,
    "timestamp" timestamp with time zone NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    task_id character varying(250) NOT NULL,
    dag_id character varying(250) NOT NULL
);


--
-- Name: xcom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.xcom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: xcom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.xcom_id_seq OWNED BY public.xcom.id;


--
-- Name: ab_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission ALTER COLUMN id SET DEFAULT nextval('public.ab_permission_id_seq'::regclass);


--
-- Name: ab_permission_view id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view ALTER COLUMN id SET DEFAULT nextval('public.ab_permission_view_id_seq'::regclass);


--
-- Name: ab_permission_view_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view_role ALTER COLUMN id SET DEFAULT nextval('public.ab_permission_view_role_id_seq'::regclass);


--
-- Name: ab_register_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_register_user ALTER COLUMN id SET DEFAULT nextval('public.ab_register_user_id_seq'::regclass);


--
-- Name: ab_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_role ALTER COLUMN id SET DEFAULT nextval('public.ab_role_id_seq'::regclass);


--
-- Name: ab_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user ALTER COLUMN id SET DEFAULT nextval('public.ab_user_id_seq'::regclass);


--
-- Name: ab_user_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user_role ALTER COLUMN id SET DEFAULT nextval('public.ab_user_role_id_seq'::regclass);


--
-- Name: ab_view_menu id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_view_menu ALTER COLUMN id SET DEFAULT nextval('public.ab_view_menu_id_seq'::regclass);


--
-- Name: chart id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chart ALTER COLUMN id SET DEFAULT nextval('public.chart_id_seq'::regclass);


--
-- Name: connection id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.connection ALTER COLUMN id SET DEFAULT nextval('public.connection_id_seq'::regclass);


--
-- Name: dag_pickle id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_pickle ALTER COLUMN id SET DEFAULT nextval('public.dag_pickle_id_seq'::regclass);


--
-- Name: dag_run id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_run ALTER COLUMN id SET DEFAULT nextval('public.dag_run_id_seq'::regclass);


--
-- Name: import_error id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.import_error ALTER COLUMN id SET DEFAULT nextval('public.import_error_id_seq'::regclass);


--
-- Name: job id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job ALTER COLUMN id SET DEFAULT nextval('public.job_id_seq'::regclass);


--
-- Name: known_event id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event ALTER COLUMN id SET DEFAULT nextval('public.known_event_id_seq'::regclass);


--
-- Name: known_event_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event_type ALTER COLUMN id SET DEFAULT nextval('public.known_event_type_id_seq'::regclass);


--
-- Name: log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log ALTER COLUMN id SET DEFAULT nextval('public.log_id_seq'::regclass);


--
-- Name: slot_pool id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slot_pool ALTER COLUMN id SET DEFAULT nextval('public.slot_pool_id_seq'::regclass);


--
-- Name: task_fail id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_fail ALTER COLUMN id SET DEFAULT nextval('public.task_fail_id_seq'::regclass);


--
-- Name: task_reschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_reschedule ALTER COLUMN id SET DEFAULT nextval('public.task_reschedule_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: variable id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variable ALTER COLUMN id SET DEFAULT nextval('public.variable_id_seq'::regclass);


--
-- Name: xcom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.xcom ALTER COLUMN id SET DEFAULT nextval('public.xcom_id_seq'::regclass);


--
-- Data for Name: ab_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_permission (id, name) FROM stdin;
\.


--
-- Data for Name: ab_permission_view; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_permission_view (id, permission_id, view_menu_id) FROM stdin;
\.


--
-- Data for Name: ab_permission_view_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_permission_view_role (id, permission_view_id, role_id) FROM stdin;
\.


--
-- Data for Name: ab_register_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_register_user (id, first_name, last_name, username, password, email, registration_date, registration_hash) FROM stdin;
\.


--
-- Data for Name: ab_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_role (id, name) FROM stdin;
\.


--
-- Data for Name: ab_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_user (id, first_name, last_name, username, password, active, email, last_login, login_count, fail_login_count, created_on, changed_on, created_by_fk, changed_by_fk) FROM stdin;
\.


--
-- Data for Name: ab_user_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_user_role (id, user_id, role_id) FROM stdin;
\.


--
-- Data for Name: ab_view_menu; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ab_view_menu (id, name) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: chart; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chart (id, label, conn_id, user_id, chart_type, sql_layout, sql, y_log_scale, show_datatable, show_sql, height, default_params, x_is_date, iteration_no, last_modified) FROM stdin;
\.


--
-- Data for Name: connection; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.connection (id, conn_id, conn_type, host, schema, login, password, port, extra, is_encrypted, is_extra_encrypted) FROM stdin;
\.


--
-- Data for Name: dag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dag (dag_id, is_paused, is_subdag, is_active, last_scheduler_run, last_pickled, last_expired, scheduler_lock, pickle_id, fileloc, owners, description, default_view, schedule_interval, root_dag_id) FROM stdin;
\.


--
-- Data for Name: dag_code; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dag_code (fileloc_hash, fileloc, source_code, last_updated) FROM stdin;
\.


--
-- Data for Name: dag_pickle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dag_pickle (id, pickle, created_dttm, pickle_hash) FROM stdin;
\.


--
-- Data for Name: dag_run; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dag_run (id, dag_id, execution_date, state, run_id, external_trigger, conf, end_date, start_date) FROM stdin;
\.


--
-- Data for Name: dag_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dag_tag (name, dag_id) FROM stdin;
\.


--
-- Data for Name: import_error; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.import_error (id, "timestamp", filename, stacktrace) FROM stdin;
\.


--
-- Data for Name: job; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.job (id, dag_id, state, job_type, start_date, end_date, latest_heartbeat, executor_class, hostname, unixname) FROM stdin;
\.


--
-- Data for Name: known_event; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.known_event (id, label, start_date, end_date, user_id, known_event_type_id, description) FROM stdin;
\.


--
-- Data for Name: known_event_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.known_event_type (id, know_event_type) FROM stdin;
\.


--
-- Data for Name: kube_resource_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kube_resource_version (one_row_id, resource_version) FROM stdin;
\.


--
-- Data for Name: kube_worker_uuid; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kube_worker_uuid (one_row_id, worker_uuid) FROM stdin;
\.


--
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.log (id, dttm, dag_id, task_id, event, execution_date, owner, extra) FROM stdin;
\.


--
-- Data for Name: rendered_task_instance_fields; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rendered_task_instance_fields (dag_id, task_id, execution_date, rendered_fields) FROM stdin;
\.


--
-- Data for Name: serialized_dag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.serialized_dag (dag_id, fileloc, fileloc_hash, data, last_updated, dag_hash) FROM stdin;
\.


--
-- Data for Name: sla_miss; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sla_miss (task_id, dag_id, execution_date, email_sent, "timestamp", description, notification_sent) FROM stdin;
\.


--
-- Data for Name: slot_pool; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.slot_pool (id, pool, slots, description) FROM stdin;
\.


--
-- Data for Name: task_fail; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.task_fail (id, task_id, dag_id, execution_date, start_date, end_date, duration) FROM stdin;
\.


--
-- Data for Name: task_instance; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.task_instance (task_id, dag_id, execution_date, start_date, end_date, duration, state, try_number, hostname, unixname, job_id, pool, queue, priority_weight, operator, queued_dttm, pid, max_tries, executor_config, pool_slots) FROM stdin;
\.


--
-- Data for Name: task_reschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.task_reschedule (id, task_id, dag_id, execution_date, try_number, start_date, end_date, duration, reschedule_date) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, username, email, password, superuser) FROM stdin;
\.


--
-- Data for Name: variable; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.variable (id, key, val, is_encrypted) FROM stdin;
\.


--
-- Data for Name: xcom; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.xcom (id, key, value, "timestamp", execution_date, task_id, dag_id) FROM stdin;
\.


--
-- Name: ab_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_permission_id_seq', 1, false);


--
-- Name: ab_permission_view_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_permission_view_id_seq', 1, false);


--
-- Name: ab_permission_view_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_permission_view_role_id_seq', 1, false);


--
-- Name: ab_register_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_register_user_id_seq', 1, false);


--
-- Name: ab_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_role_id_seq', 1, false);


--
-- Name: ab_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_user_id_seq', 1, false);


--
-- Name: ab_user_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_user_role_id_seq', 1, false);


--
-- Name: ab_view_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ab_view_menu_id_seq', 1, false);


--
-- Name: chart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chart_id_seq', 1, true);


--
-- Name: connection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.connection_id_seq', 40, true);


--
-- Name: dag_pickle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dag_pickle_id_seq', 1, false);


--
-- Name: dag_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dag_run_id_seq', 1, false);


--
-- Name: import_error_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.import_error_id_seq', 1, false);


--
-- Name: job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.job_id_seq', 1, false);


--
-- Name: known_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.known_event_id_seq', 1, false);


--
-- Name: known_event_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.known_event_type_id_seq', 4, true);


--
-- Name: log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.log_id_seq', 1, false);


--
-- Name: slot_pool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.slot_pool_id_seq', 1, true);


--
-- Name: task_fail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_fail_id_seq', 1, false);


--
-- Name: task_reschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.task_reschedule_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.variable_id_seq', 1, false);


--
-- Name: xcom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.xcom_id_seq', 1, false);


--
-- Name: ab_permission ab_permission_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission
    ADD CONSTRAINT ab_permission_name_key UNIQUE (name);


--
-- Name: ab_permission ab_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission
    ADD CONSTRAINT ab_permission_pkey PRIMARY KEY (id);


--
-- Name: ab_permission_view ab_permission_view_permission_id_view_menu_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_permission_id_view_menu_id_key UNIQUE (permission_id, view_menu_id);


--
-- Name: ab_permission_view ab_permission_view_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_pkey PRIMARY KEY (id);


--
-- Name: ab_permission_view_role ab_permission_view_role_permission_view_id_role_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_permission_view_id_role_id_key UNIQUE (permission_view_id, role_id);


--
-- Name: ab_permission_view_role ab_permission_view_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_pkey PRIMARY KEY (id);


--
-- Name: ab_register_user ab_register_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_register_user
    ADD CONSTRAINT ab_register_user_pkey PRIMARY KEY (id);


--
-- Name: ab_register_user ab_register_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_register_user
    ADD CONSTRAINT ab_register_user_username_key UNIQUE (username);


--
-- Name: ab_role ab_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_role
    ADD CONSTRAINT ab_role_name_key UNIQUE (name);


--
-- Name: ab_role ab_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_role
    ADD CONSTRAINT ab_role_pkey PRIMARY KEY (id);


--
-- Name: ab_user ab_user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_email_key UNIQUE (email);


--
-- Name: ab_user ab_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_pkey PRIMARY KEY (id);


--
-- Name: ab_user_role ab_user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_pkey PRIMARY KEY (id);


--
-- Name: ab_user_role ab_user_role_user_id_role_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_user_id_role_id_key UNIQUE (user_id, role_id);


--
-- Name: ab_user ab_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_username_key UNIQUE (username);


--
-- Name: ab_view_menu ab_view_menu_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_view_menu
    ADD CONSTRAINT ab_view_menu_name_key UNIQUE (name);


--
-- Name: ab_view_menu ab_view_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_view_menu
    ADD CONSTRAINT ab_view_menu_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: chart chart_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chart
    ADD CONSTRAINT chart_pkey PRIMARY KEY (id);


--
-- Name: connection connection_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.connection
    ADD CONSTRAINT connection_pkey PRIMARY KEY (id);


--
-- Name: dag_code dag_code_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_code
    ADD CONSTRAINT dag_code_pkey PRIMARY KEY (fileloc_hash);


--
-- Name: dag_pickle dag_pickle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_pickle
    ADD CONSTRAINT dag_pickle_pkey PRIMARY KEY (id);


--
-- Name: dag dag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag
    ADD CONSTRAINT dag_pkey PRIMARY KEY (dag_id);


--
-- Name: dag_run dag_run_dag_id_execution_date_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_run
    ADD CONSTRAINT dag_run_dag_id_execution_date_key UNIQUE (dag_id, execution_date);


--
-- Name: dag_run dag_run_dag_id_run_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_run
    ADD CONSTRAINT dag_run_dag_id_run_id_key UNIQUE (dag_id, run_id);


--
-- Name: dag_run dag_run_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_run
    ADD CONSTRAINT dag_run_pkey PRIMARY KEY (id);


--
-- Name: dag_tag dag_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_tag
    ADD CONSTRAINT dag_tag_pkey PRIMARY KEY (name, dag_id);


--
-- Name: import_error import_error_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.import_error
    ADD CONSTRAINT import_error_pkey PRIMARY KEY (id);


--
-- Name: job job_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_pkey PRIMARY KEY (id);


--
-- Name: known_event known_event_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event
    ADD CONSTRAINT known_event_pkey PRIMARY KEY (id);


--
-- Name: known_event_type known_event_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event_type
    ADD CONSTRAINT known_event_type_pkey PRIMARY KEY (id);


--
-- Name: kube_resource_version kube_resource_version_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kube_resource_version
    ADD CONSTRAINT kube_resource_version_pkey PRIMARY KEY (one_row_id);


--
-- Name: kube_worker_uuid kube_worker_uuid_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kube_worker_uuid
    ADD CONSTRAINT kube_worker_uuid_pkey PRIMARY KEY (one_row_id);


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: rendered_task_instance_fields rendered_task_instance_fields_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rendered_task_instance_fields
    ADD CONSTRAINT rendered_task_instance_fields_pkey PRIMARY KEY (dag_id, task_id, execution_date);


--
-- Name: serialized_dag serialized_dag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.serialized_dag
    ADD CONSTRAINT serialized_dag_pkey PRIMARY KEY (dag_id);


--
-- Name: sla_miss sla_miss_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sla_miss
    ADD CONSTRAINT sla_miss_pkey PRIMARY KEY (task_id, dag_id, execution_date);


--
-- Name: slot_pool slot_pool_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slot_pool
    ADD CONSTRAINT slot_pool_pkey PRIMARY KEY (id);


--
-- Name: slot_pool slot_pool_pool_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.slot_pool
    ADD CONSTRAINT slot_pool_pool_key UNIQUE (pool);


--
-- Name: task_fail task_fail_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_fail
    ADD CONSTRAINT task_fail_pkey PRIMARY KEY (id);


--
-- Name: task_instance task_instance_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_instance
    ADD CONSTRAINT task_instance_pkey PRIMARY KEY (task_id, dag_id, execution_date);


--
-- Name: task_reschedule task_reschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_reschedule
    ADD CONSTRAINT task_reschedule_pkey PRIMARY KEY (id);


--
-- Name: users user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: users user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: variable variable_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variable
    ADD CONSTRAINT variable_key_key UNIQUE (key);


--
-- Name: variable variable_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variable
    ADD CONSTRAINT variable_pkey PRIMARY KEY (id);


--
-- Name: xcom xcom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.xcom
    ADD CONSTRAINT xcom_pkey PRIMARY KEY (id);


--
-- Name: dag_id_state; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX dag_id_state ON public.dag_run USING btree (dag_id, state);


--
-- Name: idx_fileloc_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fileloc_hash ON public.serialized_dag USING btree (fileloc_hash);


--
-- Name: idx_job_state_heartbeat; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_job_state_heartbeat ON public.job USING btree (state, latest_heartbeat);


--
-- Name: idx_log_dag; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_log_dag ON public.log USING btree (dag_id);


--
-- Name: idx_root_dag_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_root_dag_id ON public.dag USING btree (root_dag_id);


--
-- Name: idx_task_fail_dag_task_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_task_fail_dag_task_date ON public.task_fail USING btree (dag_id, task_id, execution_date);


--
-- Name: idx_task_reschedule_dag_task_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_task_reschedule_dag_task_date ON public.task_reschedule USING btree (dag_id, task_id, execution_date);


--
-- Name: idx_xcom_dag_task_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_xcom_dag_task_date ON public.xcom USING btree (dag_id, task_id, execution_date);


--
-- Name: job_type_heart; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX job_type_heart ON public.job USING btree (job_type, latest_heartbeat);


--
-- Name: sm_dag; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sm_dag ON public.sla_miss USING btree (dag_id);


--
-- Name: ti_dag_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_dag_date ON public.task_instance USING btree (dag_id, execution_date);


--
-- Name: ti_dag_state; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_dag_state ON public.task_instance USING btree (dag_id, state);


--
-- Name: ti_job_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_job_id ON public.task_instance USING btree (job_id);


--
-- Name: ti_pool; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_pool ON public.task_instance USING btree (pool, state, priority_weight);


--
-- Name: ti_state; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_state ON public.task_instance USING btree (state);


--
-- Name: ti_state_lkp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_state_lkp ON public.task_instance USING btree (dag_id, task_id, execution_date, state);


--
-- Name: ti_worker_healthcheck; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ti_worker_healthcheck ON public.task_instance USING btree (end_date, hostname, state);


--
-- Name: ab_permission_view ab_permission_view_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.ab_permission(id);


--
-- Name: ab_permission_view_role ab_permission_view_role_permission_view_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_permission_view_id_fkey FOREIGN KEY (permission_view_id) REFERENCES public.ab_permission_view(id);


--
-- Name: ab_permission_view_role ab_permission_view_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- Name: ab_permission_view ab_permission_view_view_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_view_menu_id_fkey FOREIGN KEY (view_menu_id) REFERENCES public.ab_view_menu(id);


--
-- Name: ab_user ab_user_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- Name: ab_user ab_user_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- Name: ab_user_role ab_user_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- Name: ab_user_role ab_user_role_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- Name: chart chart_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chart
    ADD CONSTRAINT chart_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: dag_tag dag_tag_dag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dag_tag
    ADD CONSTRAINT dag_tag_dag_id_fkey FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id);


--
-- Name: known_event known_event_known_event_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event
    ADD CONSTRAINT known_event_known_event_type_id_fkey FOREIGN KEY (known_event_type_id) REFERENCES public.known_event_type(id);


--
-- Name: known_event known_event_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.known_event
    ADD CONSTRAINT known_event_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: task_reschedule task_reschedule_dag_task_date_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_reschedule
    ADD CONSTRAINT task_reschedule_dag_task_date_fkey FOREIGN KEY (task_id, dag_id, execution_date) REFERENCES public.task_instance(task_id, dag_id, execution_date) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM cloudsqladmin;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO cloudsqlsuperuser;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

"""


class EnvironmentUtils:
    """Utility functions for interactions with Composer environment."""

    @staticmethod
    def unique_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def read_environment_config(
        project_name: str, environment_name: str, location: str
    ) -> typing.Dict[typing.Any, typing.Any]:
        logger.info("*** Fetching details of the environment: %s...", environment_name)
        environment_json = Command.run_shell_command(
            [
                "gcloud",
                "composer",
                "environments",
                "describe",
                environment_name,
                "--project",
                project_name,
                "--location",
                location,
                "--format",
                "json",
            ]
        )
        return json.loads(environment_json)

    @staticmethod
    def get_gke_credentials(
        gke_id: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        """Gets credentials of a given GKE cluster."""
        items = gke_id.split("/")
        if (
            len(items) != 6
            or items[0] != "projects"
            or (items[2] != "zones" and items[2] != "locations")
            or items[4] != "clusters"
        ):
            raise Exception(
                f'GKE id "{gke_id}" is not an appriopriate id of GKE cluster.'
            )
        shell_command = [
            "gcloud",
            "container",
            "clusters",
            "get-credentials",
            gke_id,
            "--zone" if items[2] == "zones" else "--region",
            items[3],
        ]
        if use_private_gke_endpoint:
            shell_command.append("--internal-ip")
        Command.run_shell_command(shell_command)

    @staticmethod
    def get_pods_config() -> typing.Dict[typing.Any, typing.Any]:
        """Returns configuration of pods in given GKE cluster."""
        shell_command = [
            "kubectl",
            "get",
            "pods",
            "--all-namespaces",
            "--field-selector=status.phase=Running",
            "-o",
            "json",
        ]
        pods_json = Command.run_shell_command(shell_command)
        pods_config = json.loads(pods_json)
        return pods_config

    @staticmethod
    def get_pod_with_label(
        pods_config: typing.Dict[typing.Any, typing.Any], label: str
    ) -> typing.Dict[typing.Any, typing.Any]:
        """Returns a pod with a given label."""
        for pod_desc in pods_config["items"]:
            if (
                "run" in pod_desc["metadata"]["labels"]
                and pod_desc["metadata"]["labels"]["run"] == label
            ):
                namespace = pod_desc["metadata"]["namespace"]
                name = pod_desc["metadata"]["name"]
                logger.info(
                    "The following pod has been found: namespace = %s; name = %s",
                    namespace,
                    name,
                )
                return pod_desc
        raise Exception(
            f'Could not find any pod with label "{label}" running in the cluster.'
        )

    @staticmethod
    def get_namespace_and_name_from_pod(
        pod_desc: typing.Dict[typing.Any, typing.Any]
    ) -> typing.Tuple[str, str]:
        """Returns namespace and name of a given pod."""
        return pod_desc["metadata"]["namespace"], pod_desc["metadata"]["name"]

    @staticmethod
    def create_gke_worfload(workload_definition: str, deployment_name: str) -> str:
        """Creates a workload in GKE cluster."""
        file_name = f"deployment-{deployment_name}.yaml"
        with open(file_name, "w") as file:
            file.write(workload_definition)
        shell_command = ["kubectl", "create", "-f", file_name]
        logger.info("Creating GKE workload...")
        return Command.run_shell_command(shell_command)

    @staticmethod
    def execute_command_in_a_pod(
        namespace: str,
        pod_name: str,
        container_name: str,
        command: str,
        log_command: bool = True,
        log_error: bool = True,
    ) -> str:
        """Executes shell command in a given pod."""
        shell_command = [
            "kubectl",
            "exec",
            "-t",
            "-n",
            namespace,
            pod_name,
            "-c",
            container_name,
            "--",
            "bash",
            "-c",
            command,
        ]
        return Command.run_shell_command(
            shell_command, log_command=log_command, log_error=log_error
        )

    @staticmethod
    def read_env_variable_from_container(
        namespace: str,
        pod_name: str,
        container_name: str,
        env_name: str,
        log_env_var_value: bool = True,
    ) -> str:
        """Reads environment variable from a given container."""
        value = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"echo ${env_name}",
            log_command=log_env_var_value,
        )
        logger.info(
            'Fetch environment variable: %s = "%s"',
            env_name,
            value if log_env_var_value else "[HIDDEN]",
        )
        return value

    @staticmethod
    def grant_permissions_to_the_bucket(
        service_account: str,
        bucket_name: str,
        namespace: str,
        pod_name: str,
        container_name: str,
    ) -> None:
        """Grants objectAdmin permission to a given bucket."""
        logger.info(
            "Granting permissions for %s to access %s...", service_account, bucket_name
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gsutil iam ch serviceAccount:{service_account}:"
            f"legacyBucketWriter,legacyObjectOwner gs://{bucket_name}",
        )
        logger.info(output)

    @staticmethod
    def revoke_permissions_to_the_bucket(
        service_account: str,
        bucket_name: str,
        namespace: str,
        pod_name: str,
        container_name: str,
    ) -> None:
        """Revokes objectAdmin permission to a given bucket."""
        logger.info(
            "Revoking permissions for %s to access %s...", service_account, bucket_name
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            namespace,
            pod_name,
            container_name,
            f"gsutil iam ch -d serviceAccount:{service_account}:"
            f"legacyBucketWriter,legacyObjectOwner gs://{bucket_name}",
        )
        logger.info(output)

    @staticmethod
    def create_database_through_exising_workload(
        namespace: str,
        pod_name: str,
        container_name: str,
        sql_instance: str,
        project: str,
        database_name: str,
    ) -> str:
        """Creates new database in existing CloudSQL instance."""
        command = (
            f"gcloud sql databases create {database_name} -i {sql_instance} "
            f"--charset=utf-8 --project {project}"
        )
        return EnvironmentUtils.execute_command_in_a_pod(
            namespace, pod_name, container_name, command
        )


class DatabasePorter:
    """Common routines for exporter and importer."""

    AIRFLOW_VERSION_RE = re.compile("composer-.*-airflow-([0-9]+).([0-9]+).([0-9]+).*")

    def __init__(
        self: typing.Any,
        expected_airflow_database_version: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        self._expected_airflow_database_version = expected_airflow_database_version
        self._use_private_gke_endpoint = use_private_gke_endpoint

    def _check_environment(self: typing.Any) -> None:
        """Gathers information about the Composer environment."""
        logger.info("*** Inspecting Composer environment...")
        self.unique_id = EnvironmentUtils.unique_id()
        self._read_environment_configuration()
        self._check_airflow_version()
        self._access_gke_cluster()
        self.pods_config = EnvironmentUtils.get_pods_config()
        self._read_environment_variables_from_monitoring_pod()
        self._find_worker_pod()
        self._check_drs_and_select_db_storage_bucket()
        self._read_fernet_key()
        self.sql_service_account = (
            DatabaseUtils.fetch_cloudsql_service_account_through_the_workload(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                self.sql_instance_name,
                self.tenant_project_name,
            )
        )
        self._check_database_version()
        self._check_composer_system_namespace()
        self._check_cloud_sql_proxy()

    def _read_environment_configuration(self: typing.Any) -> None:
        logger.info("*** Reading environment configuration...")
        self.environment_config = EnvironmentUtils.read_environment_config(
            self.project_name, self.environment_name, self.location
        )
        self.gke_id = self.environment_config["config"]["gkeCluster"]
        logger.info("GKE URL: %s", self.gke_id)
        self.image_version = self.environment_config["config"]["softwareConfig"][
            "imageVersion"
        ]
        logger.info("Image version: %s", self.image_version)

    def _check_airflow_version(self: typing.Any) -> None:
        """Checks Airflow version."""
        logger.info("*** Checking Airflow version...")
        if DatabasePorter.AIRFLOW_VERSION_RE.match(self.image_version):
            v1, v2, v3 = DatabaseImporter.AIRFLOW_VERSION_RE.match(
                self.image_version
            ).groups()
            if self.is_good_airflow_version(int(v1), int(v2), int(v3)):
                return
        raise Exception(
            f"{self.bad_airflow_message} "
            f"Image version of this environment: {self.image_version}."
        )

    def _access_gke_cluster(self: typing.Any) -> None:
        """Exports custom KUBECTL and requests credentials to the GKE cluster."""
        logger.info("*** Getting credentials to GKE cluster...")
        self._kubeconfig_file_name = f"kubeconfig-{self.unique_id}"
        os.environ["KUBECONFIG"] = self._kubeconfig_file_name
        EnvironmentUtils.get_gke_credentials(
            self.gke_id,
            self._use_private_gke_endpoint,
        )

    def _remove_temporary_kubeconfig(self: typing.Any) -> None:
        """Removes temporary kubeconfig file."""
        if os.path.isfile(self._kubeconfig_file_name):
            os.remove(self._kubeconfig_file_name)

    def _grant_permissions(self: typing.Any) -> None:
        """Grants required permissions."""
        if not self.is_drs_compliant:
            logger.info("*** Granting required permissions...")
            EnvironmentUtils.grant_permissions_to_the_bucket(
                self.sql_service_account,
                self.gcs_bucket_name,
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
            )

    def _revoke_permissions(self: typing.Any) -> None:
        """Revokes no longer required permissions."""
        logger.info("*** Revoking no longer needed permissions...")
        if not self.is_drs_compliant:
            EnvironmentUtils.revoke_permissions_to_the_bucket(
                self.sql_service_account,
                self.gcs_bucket_name,
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
            )

    def _find_worker_pod(self: typing.Any) -> None:
        """Finds namespace and name of a worker pod existing in an environment."""
        logger.info("*** Finding existing worker pod...")
        self.worker_container_name = "airflow-worker"
        pod_desc = EnvironmentUtils.get_pod_with_label(
            self.pods_config, self.worker_container_name
        )
        (
            self.worker_pod_namespace,
            self.worker_pod_name,
        ) = EnvironmentUtils.get_namespace_and_name_from_pod(pod_desc)
        self.worker_pod_desc = pod_desc

    def _get_airflow_monitoring_container_description(
        self: typing.Any,
        monitoring_pod_description: typing.Dict[typing.Any, typing.Any],
    ) -> typing.Dict[typing.Any, typing.Any]:
        """Finds airflow-monitoring container in monitoring pod description."""
        for container in monitoring_pod_description["spec"]["containers"]:
            if container["name"] == "airflow-monitoring":
                return container
        raise Exception("airflow-monitoring container could not be found.")

    def _get_environment_variable_from_container_description(
        self: typing.Any,
        variable_name: str,
        container_description: typing.Dict[typing.Any, typing.Any],
    ) -> str:
        """Reads environment variable from container description"""
        for variable in container_description["env"]:
            if variable["name"] == variable_name:
                logger.info(
                    'Fetch environment variable: %s = "%s"',
                    variable_name,
                    variable["value"],
                )
                return variable["value"]
        raise KeyError(
            f"Environment variable {variable} could not be found in the container."
        )

    def _read_environment_variables_from_monitoring_pod(self: typing.Any) -> None:
        """Reads relevant environment variables from airflow-monitoring."""
        logger.info("*** Reading environment variables from airflow-monitoring pod...")
        logger.info("Finding existing monitoring pod...")
        monitoring_pod_description = EnvironmentUtils.get_pod_with_label(
            self.pods_config, "airflow-monitoring"
        )
        monitoring_container_description = (
            self._get_airflow_monitoring_container_description(
                monitoring_pod_description
            )
        )
        self.airflow_database_version = (
            self._get_environment_variable_from_container_description(
                "AIRFLOW_DATABASE_VERSION",
                monitoring_container_description,
            )
        )
        self.sql_instance_name = (
            self._get_environment_variable_from_container_description(
                "SQL_INSTANCE_NAME",
                monitoring_container_description,
            ).split(":")[1]
        )
        self.sql_database = self._get_environment_variable_from_container_description(
            "SQL_DATABASE",
            monitoring_container_description,
        )
        self.gcs_bucket_name = (
            self._get_environment_variable_from_container_description(
                "GCS_BUCKET",
                monitoring_container_description,
            )
        )
        self.cp_bucket_name = self.gcs_bucket_name
        self.tenant_project_name = (
            self._get_environment_variable_from_container_description(
                "TENANT_PROJECT",
                monitoring_container_description,
            )
        )
        try:
            self.sql_proxy = self._get_environment_variable_from_container_description(
                "SQL_HOST",
                monitoring_container_description,
            )
        except KeyError:
            self.sql_proxy = None

    def _read_fernet_key(self: typing.Any) -> None:
        self.fernet_key = EnvironmentUtils.read_env_variable_from_container(
            self.worker_pod_namespace,
            self.worker_pod_name,
            "airflow-worker",
            "AIRFLOW__CORE__FERNET_KEY",
            log_env_var_value=False,
        )

    def _check_database_version(self: typing.Any) -> None:
        """Checks database version in the environment."""
        logger.info("*** Veryfying database version...")
        if self.airflow_database_version != self._expected_airflow_database_version:
            raise Exception(
                "This operation is meant for Composer environments"
                f" with {self._expected_airflow_database_version}."
            )

    def _check_composer_system_namespace(self: typing.Any) -> None:
        """Checks existence of composer-system namespace."""
        logger.info("*** Checking if composer-system namespace exists...")
        try:
            Command.run_shell_command(
                ["kubectl", "get", "namespace", "composer-system"],
                log_command=False,
                log_error=False,
            )
            self.composer_system_namespace_exists = True
        except Exception:
            self.composer_system_namespace_exists = False

    def _check_cloud_sql_proxy(self: typing.Any) -> None:
        """Sets sql proxy."""
        if self.sql_proxy is not None:
            logger.info(
                "sql proxy as provided by SQL_HOST: %s",
                self.sql_proxy,
            )
        else:
            namespace = (
                "composer-system"
                if self.composer_system_namespace_exists
                else "default"
            )
            self.sql_proxy = f"airflow-sqlproxy-service.{namespace}.svc.cluster.local"
            logger.info(
                "composer-system %s -> sql proxy: %s",
                "exists" if self.composer_system_namespace_exists else "does not exist",
                self.sql_proxy,
            )

    def _check_drs_and_select_db_storage_bucket(self: typing.Any) -> None:
        """Checks if the environment is DRS-compliant."""
        logger.info("*** Checking if the environment is DRS-compliant...")
        self.is_drs_compliant = False
        bucket_name_prefix = self.cp_bucket_name[: -len("-bucket")]
        agent_bucket_name = f"{bucket_name_prefix}-agent"
        try:
            EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                f"gsutil ls gs://{agent_bucket_name}",
                log_command=False,
                log_error=False,
            )
            self.is_drs_compliant = True
            logger.info(
                "%s bucket has been found -> environment is DRS compliant.",
                agent_bucket_name,
            )
        except Exception as e:  # pylint: disable=broad-except
            logger.info(
                "%s bucket has not been found -> environment is not DRS compliant."
                " (%s)",
                agent_bucket_name,
                e,
            )
        if self.is_drs_compliant:
            self.gcs_bucket_name = agent_bucket_name
        logger.info("Bucket in customer project:  %s.", self.cp_bucket_name)
        logger.info("Bucket accessible from tenant project:  %s.", self.gcs_bucket_name)


class DatabaseImporter(DatabasePorter):
    """Handles import of Airflow database from CSV files."""

    EXPECTED_AIRFLOW_DATABASE_VERSION = "POSTGRES_13"
    DATABASE_CREATION_JOB_IMAGE_VERSION = "1.10.14"
    DATABASE_CREATION_JOB_IMAGE_TAG = "cloud_composer_service_2021-03-07-RC1"
    TEMPORARY_DATABASE_NAME = "temporary-database"
    SQL_PROXY_PORT = 3306

    def __init__(
        self: typing.Any,
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        super().__init__(
            DatabaseImporter.EXPECTED_AIRFLOW_DATABASE_VERSION,
            use_private_gke_endpoint,
        )
        self.project_name = project_name
        self.environment_name = environment_name
        self.location = location
        self.fernet_key_file = fernet_key_file
        self.is_good_airflow_version = (
            lambda a, b, c: True if a == 2 and (b > 0 or c >= 1) else False
        )
        self.bad_airflow_message = "Import operation supports only Airflow 2.0.1+."

    def _read_source_fernet_key(self: typing.Any) -> None:
        """Reads fernet key from source environment."""
        with open(self.fernet_key_file, mode="r") as file:
            self.fernet_key_from_source_environment = file.read().strip()

    def _fail_fast_if_path_is_not_available(self: typing.Any, path: str) -> None:
        """Fails if given path is not available in the bucket in CP."""
        command = f"gsutil ls gs://{self.cp_bucket_name}{path}"
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )

    def _fail_fast_if_there_are_no_files_to_import(self: typing.Any) -> None:
        """Fails if import files do not exist..."""
        logger.info(
            "Checking if required files exist in the bucket: %s.", self.cp_bucket_name
        )
        self._fail_fast_if_path_is_not_available("/import/tables")
        for table_name, _, _ in tables:
            self._fail_fast_if_path_is_not_available(f"/import/tables/{table_name}.csv")
        self._fail_fast_if_path_is_not_available("/import/dirs")

    def _cloud_storage_path_to_imported_table(self: typing.Any, table: str) -> None:
        """Translates table name into a path to CSV file."""
        return f"gs://{self.gcs_bucket_name}/import/tables/{table}.csv"

    def _copy_csv_files_to_tp_if_drs_compliant(self: typing.Any) -> None:
        """Copies CSV files to tenant project if DRS is enabled."""
        if self.is_drs_compliant:
            logger.info("*** Copying CSV files to tenant project...")
            command = (
                f"gsutil -m cp -r gs://{self.cp_bucket_name}/import/tables/* "
                f"gs://{self.gcs_bucket_name}/import/tables"
            )
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info(output)

    def _delete_database(self: typing.Any, database_name: str) -> None:
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            "psql postgres://root:${SQL_PASSWORD}"
            f"@{self.sql_proxy}/postgres -p {DatabaseImporter.SQL_PROXY_PORT} -t -c "
            f"'drop database \"{database_name}\" WITH (FORCE);'",
            log_command=False,
            log_error=False,
        )

    def _delete_old_temporary_database_if_exists(self: typing.Any) -> None:
        """Deletes temporary database from previous failed attempts."""
        logger.info(
            "*** Deleting temporary database created with previous failed import "
            "attempts (if exists)...",
        )
        try:
            self._delete_database(DatabaseImporter.TEMPORARY_DATABASE_NAME)
        except Command.CommandExecutionError:
            pass

    def _create_new_database(self: typing.Any) -> None:
        """Creates new database in target environment."""
        logger.info("*** Creating new database...")
        EnvironmentUtils.create_database_through_exising_workload(
            self.worker_pod_namespace,
            self.worker_pod_name,
            "airflow-worker",
            self.sql_instance_name,
            self.tenant_project_name,
            DatabaseImporter.TEMPORARY_DATABASE_NAME,
        )

    def _write_empty_af_1_10_14_psql_dump_to_a_local_file(self: typing.Any) -> None:
        """Writes an empty Airflow 1.10.14 database to a local file."""
        logger.info("Writing an empty Airflow 1.10.14 database to a local file...")
        self.temporary_file_for_psql_dump = "empty_af_1_10_14_psql_dump.sql"
        with open(self.temporary_file_for_psql_dump, mode="w") as file:
            file.write(sql_dump_of_empty_airflow_1_10_14_database_for_postgres_13)

    def _move_empty_af_1_10_14_psql_dump_to_the_import_bucket(self: typing.Any) -> None:
        """Moves an empty Airflow 1.10.14 database to import location."""
        logger.info("Moving an empty Airflow 1.10.14 database to import location...")
        Command.run_shell_command(
            [
                "kubectl",
                "cp",
                self.temporary_file_for_psql_dump,
                f"{self.worker_pod_namespace}/{self.worker_pod_name}"
                f":{self.temporary_file_for_psql_dump}",
                "-c",
                self.worker_container_name,
            ]
        )
        Command.run_shell_command(
            [
                "rm",
                "-f",
                self.temporary_file_for_psql_dump,
            ]
        )
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            f"gsutil mv {self.temporary_file_for_psql_dump} "
            f"gs://{self.gcs_bucket_name}/import/{self.temporary_file_for_psql_dump}",
        )

    def _load_empty_af_1_10_14_psql_dump_to_the_cloud_sql(self: typing.Any) -> None:
        """Loads an empty Airflow 1.10.14 database."""
        logger.info("Loading empty Airflow 1.10.14 database...")
        command = (
            f"gcloud sql import sql {self.sql_instance_name} "
            f"gs://{self.gcs_bucket_name}/import/{self.temporary_file_for_psql_dump} "
            f"--database={DatabaseImporter.TEMPORARY_DATABASE_NAME} "
            f"--project {self.tenant_project_name} "
            "-q"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _remove_empty_af_1_10_14_psql_dump_from_the_import_bucket(
        self: typing.Any,
    ) -> None:
        """Removes empty Airflow 1.10.14 database from import location."""
        logger.info("Removing empty Airflow 1.10.14 database from import location...")
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            f"gsutil rm gs://{self.gcs_bucket_name}"
            f"/import/{self.temporary_file_for_psql_dump}",
        )

    def _initialize_new_database_with_empty_af_1_10_14_psql_dump(
        self: typing.Any,
    ) -> None:
        """Initiates an empty Airflow 1.10.14 database in CloudSQL."""
        logger.info("Initializing an empty Airflow 1.10.14 database...")
        self._write_empty_af_1_10_14_psql_dump_to_a_local_file()
        self._move_empty_af_1_10_14_psql_dump_to_the_import_bucket()
        self._load_empty_af_1_10_14_psql_dump_to_the_cloud_sql()
        self._remove_empty_af_1_10_14_psql_dump_from_the_import_bucket()

    def _import_tables(self: typing.Any) -> None:
        """Imports CSV files to temporary database."""
        logger.info("*** Importing tables...")
        for table, _, _ in tables:
            logger.info('*** Importing table "%s"...', table)
            command = (
                f"gcloud sql import csv {self.sql_instance_name} "
                f"{self._cloud_storage_path_to_imported_table(table)} "
                f"--database={DatabaseImporter.TEMPORARY_DATABASE_NAME} "
                f"--project {self.tenant_project_name} "
                f"--table={table} -q --async"
            )
            operation_id = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info('*** Waiting for table "%s" to be imported...', table)
            command = (
                f"gcloud sql operations wait {operation_id} --timeout=3600 "
                f"--project {self.tenant_project_name}"
            )
            EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )

    def _rotate_fernet_key(self: typing.Any) -> None:
        """Rotates fernet key used to encrypt the secrets in the database."""
        logger.info("*** Rotating fernet key in the new database...")
        command = (
            "export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://"
            "${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}"
            f"/{DatabaseImporter.TEMPORARY_DATABASE_NAME} && "
            "export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://"
            "${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}"
            f"/{DatabaseImporter.TEMPORARY_DATABASE_NAME} && "
            "export AIRFLOW__CORE__FERNET_KEY="
            f"{self.fernet_key},{self.fernet_key_from_source_environment} "
            "&& airflow rotate-fernet-key"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
            log_command=False,
        )
        logger.info(output)

    def _fix_sequence_numbers_in_db(self: typing.Any) -> None:
        """Fixes sequence numbers used to generate sequential keys in the db."""
        logger.info("*** Fixing sequence numbers for primary keys...")
        for table, columns, fix_sequence_numbers in tables:
            if fix_sequence_numbers:
                logger.info('Fixing sequence numbers for table "%s"...', table)
                key = columns[0]
                command = (
                    "psql postgres://root:${SQL_PASSWORD}@"
                    f"{self.sql_proxy}/{DatabaseImporter.TEMPORARY_DATABASE_NAME} "
                    f"-p {DatabaseImporter.SQL_PROXY_PORT} -t -c "
                    f"\"SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('{table}', "
                    f"'{key}')), (SELECT (MAX({key}) + 1) FROM {table}), FALSE);\""
                )
                output = EnvironmentUtils.execute_command_in_a_pod(
                    self.worker_pod_namespace,
                    self.worker_pod_name,
                    self.worker_container_name,
                    command,
                )
                logger.info(output)

    def _update_airflow_db_connection(self: typing.Any) -> None:
        """Updates airflow_db entry in connection table."""
        export_db_connection_string = (
            "export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2:"
            "//${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}/"
            f"{DatabaseImporter.TEMPORARY_DATABASE_NAME} "
            "&& export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2:"
            "//${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}/"
            f"{DatabaseImporter.TEMPORARY_DATABASE_NAME}"
        )

        logger.info("Removing airflow_db connection from connections table...")
        try:
            EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                f"{export_db_connection_string} && "
                "airflow connections delete airflow_db",
            )
        except Command.CommandExecutionError:
            logger.info(
                "airflow_db connection could not be deleted. "
                "Proceeding anyways (it could not exist and this is not a "
                "problem)..."
            )

        logger.info("Creating new airflow_db connection...")
        EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            f"{export_db_connection_string} && "
            "airflow connections add airflow_db "
            "--conn-type postgres "
            "--conn-login $SQL_USER "
            '--conn-password="$SQL_PASSWORD" '
            f"--conn-host {self.sql_proxy} "
            f"--conn-port {DatabaseImporter.SQL_PROXY_PORT} "
            f"--conn-schema {self.sql_database}",
        )

    def _apply_migrations(self: typing.Any) -> None:
        """Applies database migrations (1.10.15->2.0.1) to the new database."""
        logger.info("*** Applying migrations...")
        command = (
            "export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2:"
            "//${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}/"
            f"{DatabaseImporter.TEMPORARY_DATABASE_NAME} "
            "&& export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2:"
            "//${SQL_USER}:${SQL_PASSWORD}@"
            f"{self.sql_proxy}:{DatabaseImporter.SQL_PROXY_PORT}/"
            f"{DatabaseImporter.TEMPORARY_DATABASE_NAME} "
            "&& airflow db upgrade"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _delete_old_database(self: typing.Any) -> None:
        """Deletes empty database created with the environment."""
        logger.info(
            "*** Deleting empty database created with the environment (%s)...",
            self.sql_database,
        )
        try:
            self._delete_database(self.sql_database)
        except Command.CommandExecutionError:
            logger.warning(
                "Deleting empty database failed, but trying to proceed anyway. "
                "If the database does not exist, the database transfer might still "
                "succeed."
            )

    def _import_dags_plugins_and_data(self: typing.Any) -> None:
        """Imports DAGs, plugins and data."""
        logger.info("Importing DAGs, plugins and data...")
        command = (
            f"gsutil -m cp -r gs://{self.cp_bucket_name}/import/dirs/* "
            f"gs://{self.cp_bucket_name}"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _switch_database_to_the_new_one(self: typing.Any) -> None:
        """Renames the new database to match name configured in the environment."""
        logger.info("*** Switching to the new database...")
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            "psql postgres://root:${SQL_PASSWORD}"
            f"@{self.sql_proxy}/postgres -p {DatabaseImporter.SQL_PROXY_PORT} -t -c "
            f'\'ALTER DATABASE "{DatabaseImporter.TEMPORARY_DATABASE_NAME}" '
            f'RENAME TO "{self.sql_database}";\'',
        )
        logger.info(output)

    def import_database(self: typing.Any) -> None:
        """Imports database from CSV files in environment's bucket."""
        self._check_environment()
        self._read_source_fernet_key()
        self._fail_fast_if_there_are_no_files_to_import()
        self._copy_csv_files_to_tp_if_drs_compliant()
        self._delete_old_temporary_database_if_exists()
        self._create_new_database()
        try:
            self._grant_permissions()
            self._initialize_new_database_with_empty_af_1_10_14_psql_dump()
            self._import_tables()
        finally:
            self._revoke_permissions()
        self._fix_sequence_numbers_in_db()
        self._apply_migrations()
        self._rotate_fernet_key()
        self._update_airflow_db_connection()
        self._delete_old_database()
        self._import_dags_plugins_and_data()
        self._switch_database_to_the_new_one()
        self._remove_temporary_kubeconfig()
        logger.info("*** Database transfer completed.")


class DatabaseExporter(DatabasePorter):
    """Handles export of Airflow database to CSV files."""

    EXPECTED_AIRFLOW_DATABASE_VERSION = "MYSQL_5_7"

    WHAT_TO_DO_NEXT = """\
Exported database, DAGs, plugins and data are now stored in
gs://{cp_bucket_name}/export.
You may now copy exported files to the target environment, e.g. with:
gsutil -m cp -r gs://{cp_bucket_name}/export gs://[TARGET ENV BUCKET NAME]/import

Once the files are copied, you may import the data through
python3 composer_db_transfer.py import ...
"""

    def __init__(
        self: typing.Any,
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        super().__init__(
            DatabaseExporter.EXPECTED_AIRFLOW_DATABASE_VERSION,
            use_private_gke_endpoint,
        )
        self.project_name = project_name
        self.environment_name = environment_name
        self.location = location
        self.fernet_key_file = fernet_key_file
        self.is_good_airflow_version = (
            lambda a, b, c: True if a == 1 and b == 10 and c >= 14 else False
        )
        self.bad_airflow_message = (
            "Export operation supports only Airflow 1.10.x, x >= 14."
        )

    def _cloud_storage_path_to_exported_table(self: typing.Any, table: str) -> str:
        """Translates table name into a path to CSV file in a bucket."""
        return f"gs://{self.gcs_bucket_name}/export/tables/{table}.csv"

    def _mounted_path_to_exported_table(self: typing.Any, table: str) -> str:
        """Translates table name into a path to CSV file available in worker pod."""
        return f"/home/airflow/gcsfuse/export/tables/{table}.csv"

    def _export_table_to_csv_with_custom_query(
        self: typing.Any, table: str, select_query: str
    ) -> None:
        """Exports a given table to CSV file through provided SELECT query."""
        logger.info("Exporting table %s...", table)
        command = (
            f"gcloud sql export csv {self.sql_instance_name} "
            f"{self._cloud_storage_path_to_exported_table(table)} "
            f"--database={self.sql_database} --project {self.tenant_project_name} "
            f"'--query={select_query}'"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _post_process_exported_table(self: typing.Any, table: str) -> None:
        """Performs post processing of exported CSV files."""
        logger.info("Postprocessing exported table: %s...", table)
        command = (
            f"sed -e s/'\"{DatabaseUtils.null_string}\"'//g "
            f"-i {self._mounted_path_to_exported_table(table)}"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _export_tables(self: typing.Any) -> None:
        """Exports all tables to CSV files in the environment's bucket."""
        logger.info("Exporting tables...")
        for table, columns, _ in tables:
            columns_expression = ", ".join(columns)
            select_query = f"SELECT {columns_expression} from {table};"
            self._export_table_to_csv_with_custom_query(table, select_query)

    def _postprocess_tables(self: typing.Any) -> None:
        """Performs postprocessing of exported tables."""
        logger.info("Exporting tables...")
        for table, _, _ in tables:
            self._post_process_exported_table(table)

    def _copy_csv_files_to_cp_if_drs_compliant(self: typing.Any) -> None:
        """Copies CSV files to customer's project for DRS-compliant env."""
        if self.is_drs_compliant:
            logger.info("*** Copying CSV files to customer's project...")
            command = (
                f"gsutil -m cp -r gs://{self.gcs_bucket_name}/export/tables/* "
                f"gs://{self.cp_bucket_name}/export/tables"
            )
            output = EnvironmentUtils.execute_command_in_a_pod(
                self.worker_pod_namespace,
                self.worker_pod_name,
                self.worker_container_name,
                command,
            )
            logger.info(output)

    def _export_dags_plugins_and_data(self: typing.Any) -> None:
        """Exports DAGs, plugins and data."""
        logger.info("Exporting DAGs, plugins and data...")
        bucket = self.cp_bucket_name
        command = (
            f"gsutil -m cp -r gs://{bucket}/dags "
            f"gs://{bucket}/export/dirs/dags && "
            f"gsutil -m cp -r gs://{bucket}/plugins "
            f"gs://{bucket}/export/dirs/plugins"
            f" && gsutil -m cp -r gs://{bucket}/data "
            f"gs://{bucket}/export/dirs/data"
        )
        output = EnvironmentUtils.execute_command_in_a_pod(
            self.worker_pod_namespace,
            self.worker_pod_name,
            self.worker_container_name,
            command,
        )
        logger.info(output)

    def _save_fernet_key(self: typing.Any) -> None:
        logger.info("Saving fernet key to the file: %s", self.fernet_key_file)
        with open(self.fernet_key_file, "w") as file:
            file.write(self.fernet_key)

    def _let_them_know_about_next_steps(self: typing.Any) -> None:
        """Prints guidance about next steps to the log."""
        logger.info("*** Database export completed.")
        logger.info(
            "%s",
            DatabaseExporter.WHAT_TO_DO_NEXT.format(cp_bucket_name=self.cp_bucket_name),
        )

    def export_database(self: typing.Any) -> None:
        """Exports the database to CSV files in the environment's bucket."""
        self._check_environment()
        try:
            self._grant_permissions()
            self._export_tables()
        finally:
            self._revoke_permissions()
        self._copy_csv_files_to_cp_if_drs_compliant()
        self._postprocess_tables()
        self._export_dags_plugins_and_data()
        self._remove_temporary_kubeconfig()
        self._save_fernet_key()
        self._let_them_know_about_next_steps()


class ComposerDatabaseMigration:
    """Triggers selected operation (import/export)."""

    @staticmethod
    def export_database(
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        """Exports Airflow database to the bucket in customer's project."""
        database_importer = DatabaseExporter(
            project_name,
            environment_name,
            location,
            fernet_key_file,
            use_private_gke_endpoint,
        )
        database_importer.export_database()

    @staticmethod
    def import_database(
        project_name: str,
        environment_name: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        """Imports Airflow database from the bucket in customer's project."""
        database_importer = DatabaseImporter(
            project_name,
            environment_name,
            location,
            fernet_key_file,
            use_private_gke_endpoint,
        )
        database_importer.import_database()

    @staticmethod
    def trigger_operation(
        operation: str,
        project: str,
        environment: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        """Triggers selected operation (import/export)."""
        logger.info("Database migration script for Cloud Composer")
        if operation == "export":
            ComposerDatabaseMigration.export_database(
                project,
                environment,
                location,
                fernet_key_file,
                use_private_gke_endpoint,
            )
        elif operation == "import":
            ComposerDatabaseMigration.import_database(
                project,
                environment,
                location,
                fernet_key_file,
                use_private_gke_endpoint,
            )
        else:
            logger.error("Operation %s is not supported.", operation)

    @staticmethod
    def main(
        operation: str,
        project: str,
        environment: str,
        location: str,
        fernet_key_file: str,
        use_private_gke_endpoint: bool,
    ) -> None:
        logger.info("Database transfer tool for Cloud Composer v.%s", SCRIPT_VERSION)
        try:
            ComposerDatabaseMigration.trigger_operation(
                operation,
                project,
                environment,
                location,
                fernet_key_file,
                use_private_gke_endpoint,
            )
            exit(0)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(
                "*** Operation %s failed due to the following error:\n\n%s\n\n",
                operation,
                e,
            )
            logger.info(
                'Check "Troubleshooting" section of the script manual for '
                "troubleshooting guidance."
            )
            exit(1)


def parse_arguments() -> typing.Dict[typing.Any, typing.Any]:
    """Parses command line parameters."""
    argument_parser = argparse.ArgumentParser(
        usage=f"Database transfer tool for Cloud Composer v.{SCRIPT_VERSION}.\n\n"
        + USAGE
        + "\n"
    )
    argument_parser.add_argument("operation", type=str, choices=["import", "export"])
    argument_parser.add_argument("--project", type=str, required=True)
    argument_parser.add_argument("--environment", type=str, required=True)
    argument_parser.add_argument("--location", type=str, required=True)
    argument_parser.add_argument("--fernet-key-file", type=str, required=True)
    argument_parser.add_argument(
        "--use-private-gke-endpoint", required=False, action="store_true"
    )
    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    ComposerDatabaseMigration.main(
        args.operation,
        args.project,
        args.environment,
        args.location,
        args.fernet_key_file,
        args.use_private_gke_endpoint,
    )
