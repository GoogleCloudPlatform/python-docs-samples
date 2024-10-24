import conftest as conftest  # python-docs-samples/alloydb/conftest.py
import uuid


# def inject_password(source: str, password: str) -> str:
#     """Injects the provided password into the notebook source."""
#     modified_source = source.replace(
#         "password = input(...)", f"password = '{password}'"
#     )
#     return modified_source
CLUSTER_NAME = f"my-cluster-{uuid.uuid4()}"

def test_batch_embeddings_update(project: str) -> None:
    # TODO: Inject password such that we can take user input
    conftest.run_notebook(
        "alloydb/notebooks/batch_embeddings_update.ipynb",
        # section="### Connect Your Google Cloud Project",
        variables= {
            "project_id": project,
            # "cluster_name": CLUSTER_NAME,
            "cluster_name": "my-cluster-171930bf-d6e4-4cf8-b1fa-4538a01b9c3f",
            "password": "test_password",
        },
        until_end=True,
    )
    # Delete AlloyDB cluster
    # conftest.clean_up_cluster(cluster_name=CLUSTER_NAME)