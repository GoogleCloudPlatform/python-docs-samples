# Deployment Preview Cloud Build Configuration

These configurations aren't used by this repo itself, but are configurations required to use the code in this repo. 

 * [cloudbuild.yaml](cloudbuild.yaml) - for main branch pushes
 * [cloudbuild-preview.yaml](cloudbuild-preview.yaml) - for GitHub Pull Requests
 * [cloudbuild-cleanup.yaml](cloudbuild-cleanup.yaml) - for main branch pushes, including cleanup of old tags
