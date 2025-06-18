# Deployment Guide

This guide will help you deploy the Motivation Bot to various platforms.

## Quick Start

### 1. Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd motivation_bot

# Run the deployment script
python deploy.py

# Start the web application
python app.py
```

### 2. GitHub Repository Setup

1. **Create a new repository on GitHub**
2. **Upload your code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

## Deployment Platforms

### Heroku Deployment

1. **Install Heroku CLI** from https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set INSTAGRAM_USERNAME=your_username
   heroku config:set INSTAGRAM_PASSWORD=your_password
   heroku config:set SECRET_KEY=your-secret-key
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **Open the app:**
   ```bash
   heroku open
   ```

### Railway Deployment

1. **Go to Railway.app** and sign up with GitHub
2. **Create a new project** and select "Deploy from GitHub repo"
3. **Select your repository**
4. **Add environment variables:**
   - `INSTAGRAM_USERNAME`
   - `INSTAGRAM_PASSWORD`
   - `SECRET_KEY`
5. **Deploy automatically** - Railway will detect the Python app

### Render Deployment

1. **Go to Render.com** and sign up
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
5. **Add environment variables**
6. **Deploy**

### Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t motivation-bot .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 \
     -e INSTAGRAM_USERNAME=your_username \
     -e INSTAGRAM_PASSWORD=your_password \
     -e SECRET_KEY=your-secret-key \
     motivation-bot
   ```

3. **For production with Docker Compose:**
   ```yaml
   # docker-compose.yml
   version: '3.8'
   services:
     motivation-bot:
       build: .
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

## Environment Variables

For deployment, you'll need to set these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `INSTAGRAM_USERNAME` | Your Instagram username | Yes |
| `INSTAGRAM_PASSWORD` | Your Instagram password | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `PORT` | Port to run the app on | No (default: 5000) |

## Security Considerations

1. **Never commit sensitive data** like `config.json` to Git
2. **Use environment variables** for credentials in production
3. **Enable 2FA** on your Instagram account
4. **Use app passwords** if 2FA is enabled
5. **Regularly rotate** your Instagram password

## Troubleshooting

### Common Deployment Issues

1. **Build fails:**
   - Check if all dependencies are in `requirements.txt`
   - Ensure Python version is compatible (3.8+)

2. **App crashes on startup:**
   - Check environment variables are set correctly
   - Verify Instagram credentials are valid
   - Check logs for specific error messages

3. **Instagram login fails:**
   - Ensure 2FA is disabled or use app passwords
   - Check if account is not restricted
   - Try logging in manually first

4. **Video generation fails:**
   - Ensure OpenCV dependencies are installed
   - Check available disk space
   - Verify font files are available

### Platform-Specific Issues

#### Heroku
- **H10 App Crashed:** Check build logs and environment variables
- **H14 No Web Processes:** Ensure Procfile is present and correct
- **R10 Boot Timeout:** Optimize app startup time

#### Railway
- **Build Timeout:** Check if all dependencies are properly specified
- **Environment Variables:** Ensure all required variables are set

#### Docker
- **Permission Issues:** Check file permissions in mounted volumes
- **Port Conflicts:** Ensure port 5000 is available

## Monitoring and Maintenance

1. **Check logs regularly** for errors
2. **Monitor Instagram account** for any restrictions
3. **Update dependencies** periodically
4. **Backup generated videos** regularly
5. **Monitor disk space** usage

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify all configuration is correct
3. Test locally first
4. Check platform-specific documentation
5. Open an issue on GitHub with detailed information

## Updates

To update your deployed application:

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Redeploy:**
   - **Heroku:** `git push heroku main`
   - **Railway:** Automatic on push to main
   - **Render:** Automatic on push to main
   - **Docker:** Rebuild and restart container

Remember to test updates locally before deploying to production! 