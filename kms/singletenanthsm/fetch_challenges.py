import gcloud_commands


test_proposal_resource = "projects/cloudkms-dev/locations/us-central1/singleTenantHsmInstances/brandonluong2/proposals/3389a96c-8a64-4bd5-9b97-6957f882416f"

def test_fetch_challenges():
    process = gcloud_commands.fetch_challenges(test_proposal_resource)
    return process
    # assert not process.stderr

if __name__ == "__main__":
    challenges = test_fetch_challenges()
    print(challenges)