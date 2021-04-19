def _setup_bundle():
    from google.cloud import firestore
    db = firestore.Client()
    db.collection("stories").document("news-item").set({"title": "Wow!"})

def create_and_build_bundle():
    _setup_bundle()
    # [START fs_create_and_builde_bundle]
    from google.cloud import firestore
    from google.cloud.firestore_bundle import FirestoreBundle

    db = firestore.Client()
    bundle = FirestoreBundle("latest-stories")

    doc_snapshot = db.collection("stories").document("news-item").get()
    query = db.collection("stories")._query()

    # Build the bundle
    # Note how `query` is named "latest-stories-query"
    bundle_buffer: str = bundle.add_document(doc_snapshot).add_named_query(
        "latest-stories-query", query,
    ).build()
    # [END fs_create_and_builde_bundle]

    return bundle, bundle_buffer


def test_create_and_build_bundle():
    bundle, _ = create_and_build_bundle()
    assert "latest-stories-query" in bundle.named_queries

test_create_and_build_bundle()