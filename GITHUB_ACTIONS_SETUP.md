# GitHub Actions Setup Guide

This guide will help you set up automated deployment using GitHub Actions for your Motivation Bot.

## 🚀 Available Workflows

### 1. **Test Workflow** (`test.yml`)
- Runs on every push and pull request
- Tests code quality and functionality
- Ensures all dependencies work correctly

### 2. **Railway Deployment** (`deploy-railway.yml`)
- Automatically deploys to Railway on push to main
- Requires Railway token and service ID

### 3. **Render Deployment** (`deploy-render.yml`)
- Automatically deploys to Render on push to main
- Requires Render token and service ID

### 4. **Heroku Deployment** (`deploy-heroku.yml`)
- Automatically deploys to Heroku on push to main
- Requires Heroku API key and app name

### 5. **Docker Build** (`docker-build.yml`)
- Builds and pushes Docker images to GitHub Container Registry
- Creates images for every push and release

## 🔐 Setting Up Secrets

### Step 1: Access Repository Settings
1. Go to your GitHub repository
2. Click on **Settings** tab
3. Click on **Secrets and variables** → **Actions**

### Step 2: Add Required Secrets

#### For Railway Deployment:
```
RAILWAY_TOKEN=your_railway_token
RAILWAY_SERVICE=your_service_id
```

**How to get Railway token:**
1. Go to [Railway.app](https://railway.app)
2. Click on your profile → **Account Settings**
3. Go to **Tokens** tab
4. Create a new token

**How to get Service ID:**
1. Go to your Railway project
2. Click on your service
3. Go to **Settings** tab
4. Copy the **Service ID**

#### For Render Deployment:
```
RENDER_TOKEN=your_render_token
RENDER_SERVICE_ID=your_service_id
```

**How to get Render token:**
1. Go to [Render.com](https://render.com)
2. Click on your profile → **Account Settings**
3. Go to **API Keys** tab
4. Create a new API key

**How to get Service ID:**
1. Go to your Render dashboard
2. Click on your service
3. Copy the **Service ID** from the URL or settings

#### For Heroku Deployment:
```
HEROKU_API_KEY=your_heroku_api_key
HEROKU_APP_NAME=your_app_name
HEROKU_EMAIL=your_heroku_email
```

**How to get Heroku API key:**
1. Go to [Heroku.com](https://heroku.com)
2. Click on your profile → **Account Settings**
3. Go to **API Key** section
4. Copy your API key

## 🌐 Environment Variables for Deployment

### Railway Environment Variables:
1. Go to your Railway project
2. Click on your service
3. Go to **Variables** tab
4. Add these variables:
   ```
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   SECRET_KEY=your_secret_key
   PORT=5000
   ```

### Render Environment Variables:
1. Go to your Render dashboard
2. Click on your service
3. Go to **Environment** tab
4. Add these variables:
   ```
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   SECRET_KEY=your_secret_key
   PORT=5000
   ```

### Heroku Environment Variables:
```bash
heroku config:set INSTAGRAM_USERNAME=your_instagram_username
heroku config:set INSTAGRAM_PASSWORD=your_instagram_password
heroku config:set SECRET_KEY=your_secret_key
```

## 🔄 Workflow Triggers

### Automatic Deployment:
- **Push to main branch**: Triggers deployment
- **Pull request to main**: Runs tests only
- **Release tags**: Triggers Docker build and deployment

### Manual Deployment:
You can also trigger workflows manually:
1. Go to **Actions** tab in your repository
2. Select the workflow you want to run
3. Click **Run workflow**

## 📊 Monitoring Deployments

### Check Workflow Status:
1. Go to **Actions** tab in your repository
2. Click on the workflow run
3. View detailed logs and status

### Deployment URLs:
- **Railway**: `https://your-app-name.railway.app`
- **Render**: `https://your-app-name.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`

## 🐳 Docker Deployment

### Using GitHub Container Registry:
After Docker workflow runs, you can deploy using:
```bash
docker run -p 5000:5000 \
  -e INSTAGRAM_USERNAME=your_username \
  -e INSTAGRAM_PASSWORD=your_password \
  -e SECRET_KEY=your_secret_key \
  ghcr.io/yourusername/instagram-motivation-bot:main
```

### Using Docker Compose:
```yaml
version: '3.8'
services:
  motivation-bot:
    image: ghcr.io/yourusername/instagram-motivation-bot:main
    ports:
      - "5000:5000"
    environment:
      - INSTAGRAM_USERNAME=${INSTAGRAM_USERNAME}
      - INSTAGRAM_PASSWORD=${INSTAGRAM_PASSWORD}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./generated_videos:/app/generated_videos
      - ./music:/app/music
```

## 🔧 Troubleshooting

### Common Issues:

1. **Workflow fails on test step:**
   - Check if all dependencies are in `requirements.txt`
   - Ensure Python version is compatible
   - Check test logs for specific errors

2. **Deployment fails:**
   - Verify secrets are correctly set
   - Check if target platform is accessible
   - Ensure environment variables are set on target platform

3. **Docker build fails:**
   - Check Dockerfile syntax
   - Ensure all required files are present
   - Verify Docker context is correct

### Debugging:
1. Check workflow logs in **Actions** tab
2. Verify secrets are set correctly
3. Test locally before pushing
4. Check platform-specific logs

## 📈 Best Practices

1. **Always test locally** before pushing
2. **Use feature branches** for development
3. **Review pull requests** before merging
4. **Monitor deployment logs** regularly
5. **Keep secrets secure** and rotate them periodically
6. **Use semantic versioning** for releases

## 🎯 Quick Start Checklist

- [ ] Set up repository secrets
- [ ] Configure environment variables on target platform
- [ ] Test workflow locally
- [ ] Push to main branch to trigger deployment
- [ ] Monitor deployment status
- [ ] Verify application is running

## 📞 Support

If you encounter issues:
1. Check workflow logs in GitHub Actions
2. Verify all secrets and environment variables
3. Test the application locally
4. Check platform-specific documentation
5. Open an issue in the repository

Your motivation bot will now automatically deploy whenever you push changes to the main branch! 🚀 