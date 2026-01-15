#!/bin/bash

# Deploy script for Prerane Education System
# Project: prerane-education-system
# Region: us-central1

PROJECT_ID="prerane-education-system"
SERVICE_NAME="assignment-tracker-app"
REGION="us-central1"
DB_INSTANCE="assignment-tracker-db"
CONNECTION_NAME="$PROJECT_ID:$REGION:$DB_INSTANCE"

echo "🚀 Deploying Prerane Education System..."

# Build and push container image
echo "Building and pushing container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-cloudsql-instances $CONNECTION_NAME \
    --set-env-vars "CLOUD_SQL_CONNECTION_NAME=$CONNECTION_NAME" \
    --set-env-vars "DB_USER=django-user" \
    --set-env-vars "DB_NAME=assignment_tracker_db" \
    --set-env-vars "SECRET_KEY=krishna-shrinidhi-nadiger-katti" \
    --set-secrets "DB_PASSWORD=DB_PASSWORD:latest" \
    --project $PROJECT_ID

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🌐 Application URL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)' --project $PROJECT_ID