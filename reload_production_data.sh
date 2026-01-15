#!/bin/bash

# Production Data Reload Script for Prerane Education System
# This script clears all existing data and loads fresh data from Excel files

PROJECT_ID="prerane-education-system"
REGION="us-central1"
SERVICE_NAME="assignment-tracker-app"
CONNECTION_NAME="$PROJECT_ID:$REGION:assignment-tracker-db"

echo "🚀 Reloading production database..."
echo "⚠️  This will clear ALL existing data and load fresh data from Excel files"
echo ""
read -p "Are you sure you want to proceed? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo "Starting production data reload sequence..."

# Step 1: Clear all existing data
echo "Step 1: Clearing all existing data..."
gcloud run jobs execute clear-all-data-job --region $REGION --project $PROJECT_ID --wait

if [ $? -ne 0 ]; then
    echo "❌ Failed to clear data. Exiting."
    exit 1
fi

# Step 2: Load fresh data from Excel files
echo "Step 2: Loading fresh data from Excel files..."
gcloud run jobs execute load-fresh-data-job --region $REGION --project $PROJECT_ID --wait

if [ $? -ne 0 ]; then
    echo "❌ Failed to load data. Exiting."
    exit 1
fi

echo ""
echo "🎉 Production data reload completed successfully!"
echo ""
echo "📊 Data loaded:"
echo "   • 1 District (Belagavi)"
echo "   • Multiple Talukas"  
echo "   • Schools from school_list.xlsx"
echo "   • Students from student_list.xlsx"
echo "   • User accounts (DDPI, BEOs, Principals)"
echo ""
echo "🔑 Login credentials:"
echo "   • Superuser: superadmin / wrecK_567*"
echo "   • DDPI: belagavi_ddpi / ddpi@0831"
echo "   • BEO: {taluka_name} / {reverse_taluka_name}"
echo "   • Principal: {udise_code} / {reverse_udise_code}"
echo ""
echo "📧 All users have @prerane.in email addresses"
echo "⚠️  All users should change their passwords after first login"