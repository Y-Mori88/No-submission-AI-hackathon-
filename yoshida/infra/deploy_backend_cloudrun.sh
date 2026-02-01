#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="subsidy-api"
REGION="asia-northeast1"

gcloud run deploy "$SERVICE_NAME" \
  --source ../backend \
  --region "$REGION" \
  --allow-unauthenticated
