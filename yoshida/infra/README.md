# infra

## Backend (Cloud Run)

- Source deploy: gcloud run deploy --source backend

## Required

- gcloud auth login
- gcloud config set project <PROJECT_ID>

## Env

- GCP_PROJECT
- GCP_REGION
- GEMINI_MODEL
- ALLOW_ORIGINS (frontend url)
