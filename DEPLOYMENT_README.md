# Prerane Education System - Deployment Guide

## 📋 Project Information
- **Project ID**: `prerane-education-system`
- **Region**: `us-central1` (Iowa)
- **Database**: Cloud SQL PostgreSQL in `us-central1`
- **Application**: Cloud Run in `us-central1`
- **Domain**: `prerane.in`

## 🌐 Application URLs
- **Production App**: https://prerane.in ✅
- **Backup URL**: https://assignment-tracker-app-2ntqy2wyba-uc.a.run.app
- **Admin Panel**: https://prerane.in/admin/
- **Login**: https://prerane.in/login/

## 🔑 Login Credentials
- **Superuser**: `superadmin` / `wrecK_567*`
- **DDPI**: `ddpi` / `Ddpi@0831`
- **BEO Example**: `Beo_khanapur` / `Beo@08336`
- **Principal Example**: Use school UDISE code / reverse UDISE code

## 🚀 Deployment Commands

### For Application Changes (UI, Code Updates)
```bash
# Simple redeploy for code changes - takes 2-3 minutes
./deploy_us_central.sh
```
**Use this for:** UI changes, view updates, template modifications, code fixes

### For Database Schema Changes (New Models, Migrations)
```bash
# Deploy application first
./deploy_us_central.sh

# Then run migrations (create job once, reuse later)
gcloud run jobs execute migrate-job --region us-central1 --project prerane-education-system
```
**Use this for:** New Django models, database field changes, migrations

### For Data Reloading (⚠️ Use with Caution)
```bash
# Reload all data - WARNING: Creates duplicates if run multiple times
./reload_data.sh
```
**⚠️ IMPORTANT:** This script does NOT clear existing data first. It will:
- Add new data on top of existing data
- Create duplicate students, schools, and user accounts
- Should only be used if you need to reload data for specific reasons

## 🧹 Clear Data Before Reloading (If Needed)

If you need to clear existing data before reloading:

```bash
# Connect to production database
gcloud sql connect assignment-tracker-db --user=django-user --project=prerane-education-system

# Clear data tables (run these SQL commands)
DELETE FROM core_student;
DELETE FROM core_school WHERE id > 0;
DELETE FROM core_taluka WHERE id > 0;
DELETE FROM auth_user WHERE username != 'superadmin';

# Exit database connection
\q

# Now run reload script
./reload_data.sh
```

**Data Loading Sequence (what reload_data.sh does):**
1. `python manage.py migrate` - Apply any new migrations
2. `python manage.py import_belagavi_data 'Belagavi dist FLN list.xlsx'`
3. `python manage.py update_schools_data 'Govt Schools list2.xlsx'`
4. `python manage.py verify_import`
5. `python manage.py cleanup_duplicate_talukas`
6. `python manage.py create_custom_user_accounts`

## 🌐 Custom Domain Setup

### Test Domain Mapping Support
```bash
gcloud beta run domain-mappings create \
    --service assignment-tracker-app \
    --domain prerane.in \
    --region us-central1 \
    --project prerane-education-system
```

### If Domain Mapping Works
1. **Get DNS records**:
```bash
gcloud beta run domain-mappings describe prerane.in \
    --region us-central1 \
    --project prerane-education-system
```

2. **Add DNS records in GoDaddy**:
   - Add the A records and CNAME records provided by the command above

### If Domain Mapping Doesn't Work (Use Cloudflare - FREE)
1. **Change nameservers** to Cloudflare in GoDaddy
2. **Add CNAME record** in Cloudflare: `prerane.in` → `assignment-tracker-app-2ntqy2wyba-uc.a.run.app`
3. **Enable proxy** (orange cloud icon)
4. **Update Django settings** to allow Cloudflare domain

## 📊 Monitoring and Logs

### View Application Logs
```bash
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=assignment-tracker-app" --project=prerane-education-system --limit=50
```

### Access Database
```bash
gcloud sql connect assignment-tracker-db --user=django-user --project=prerane-education-system
```

### Check Application Status
```bash
gcloud run services describe assignment-tracker-app --region us-central1 --project prerane-education-system
```

## 🛠️ Troubleshooting

### Common Issues

1. **500 Error**: Check if migrations are applied
2. **Database Connection**: Verify Cloud SQL instance is running
3. **Permission Issues**: Check service account has Secret Manager access
4. **Build Failures**: Check Dockerfile and requirements.txt

### Quick Health Check
```bash
# Check if app is running
curl -I https://assignment-tracker-app-2ntqy2wyba-uc.a.run.app

# Check database connectivity
gcloud sql instances describe assignment-tracker-db --project=prerane-education-system
```

## 🗂️ Project Structure
```
├── deploy_us_central.sh          # Main deployment script
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
├── .dockerignore                 # Files to exclude from build
├── education_management_system/
│   ├── settings.py              # Local development settings
│   └── settings_production.py  # Production settings
└── core/                        # Django application
```

## 💰 Cost Monitoring
- **Cloud Run**: Pay per request (~$0.40 per million requests)
- **Cloud SQL**: db-f1-micro instance (~$7-15/month)
- **Cloud Build**: 120 free builds/day
- **Secret Manager**: $0.06 per 10,000 operations

## 🔐 Security Notes
- Database password stored in Google Secret Manager
- HTTPS enabled by default on Cloud Run
- Service account has minimal required permissions
- CSRF protection configured for custom domain

---

## Quick Reference Commands

**Deploy application changes (most common):**
```bash
./deploy_us_central.sh
```

**Reload all data (⚠️ creates duplicates):**
```bash
./reload_data.sh
```

**Clear data before reloading:**
```bash
# Connect to DB and run DELETE commands, then ./reload_data.sh
gcloud sql connect assignment-tracker-db --user=django-user --project=prerane-education-system
```

**View application logs:**
```bash
gcloud logs read "resource.type=cloud_run_revision" --project=prerane-education-system --limit=20
```

**Check domain mapping status:**
```bash
gcloud beta run domain-mappings describe --domain=prerane.in --region=us-central1 --project=prerane-education-system
```

**Test DNS resolution:**
```bash
nslookup prerane.in
```