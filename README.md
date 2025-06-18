# Instagram Motivation Bot

This bot automatically finds trending motivational quotes, creates short videos, and posts them to Instagram while tracking everything in an Excel file. Now with a beautiful web interface!

## Features

- **Web Interface**: Modern, responsive web UI for easy management
- **AI-Powered Quotes**: Generates motivational quotes using Ollama LLM
- **Video Generation**: Creates engaging videos with custom text overlays
- **Instagram Automation**: Posts videos to Instagram automatically
- **Music Support**: Upload custom background music for videos
- **Video Management**: Download individual videos or all videos as a zip
- **Tracking System**: Tracks all ideas and posting status in CSV/Excel
- **Completely Free**: No paid services required

## Quick Start

### Option 1: Web Interface (Recommended)

1. Install Python 3.8 or higher
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `config.json` file in the project root with your Instagram credentials:
   ```json
   {
     "instagram": {
       "username": "your_username",
       "password": "your_password"
     }
   }
   ```

4. Start the web interface:
   ```
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

### Option 2: Command Line Interface

1. Follow steps 1-3 above
2. Run the bot directly:
   ```
   python motivation_bot.py
   ```

## Web Interface Features

### Dashboard
- **Bot Status**: Monitor if the Instagram bot is running
- **Video Generation**: Create single or multiple videos with custom quotes
- **Music Upload**: Add custom background music for your videos
- **Video Management**: View, download, and manage all generated videos

### Video Generation
- Generate videos with AI-powered quotes or your own custom quotes
- Create multiple videos in batch (up to 20 at once)
- Real-time progress tracking
- Automatic video list refresh

### Bot Control
- Start/stop the Instagram automation bot
- Real-time status monitoring
- Automatic credential validation

## Deployment Options

### Local Development
```bash
python app.py
```

### Heroku Deployment
1. Create a Heroku account
2. Install Heroku CLI
3. Run these commands:
   ```bash
   heroku create your-app-name
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python app
3. Add environment variables for Instagram credentials

### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t motivation-bot .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 motivation-bot
   ```

## Configuration

### Instagram Credentials
Create a `config.json` file:
```json
{
  "instagram": {
    "username": "your_instagram_username",
    "password": "your_instagram_password"
  }
}
```

### Environment Variables (for deployment)
- `INSTAGRAM_USERNAME`: Your Instagram username
- `INSTAGRAM_PASSWORD`: Your Instagram password
- `SECRET_KEY`: Flask secret key for sessions

## File Structure

```
motivation_bot/
├── app.py                 # Flask web application
├── motivation_bot.py      # Core bot functionality
├── templates/
│   └── index.html        # Web interface template
├── config.json           # Instagram credentials
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version specification
├── generated_videos/    # Output video directory
├── music/              # Background music directory
└── motivation_ideas.csv # Tracking file
```

## How it Works

1. **Quote Generation**: Uses Ollama LLM to generate motivational quotes
2. **Video Creation**: Creates videos with text overlays using OpenCV and PIL
3. **Instagram Posting**: Automatically posts videos with captions and hashtags
4. **Tracking**: Records all activities in CSV file for monitoring

## API Endpoints

- `GET /` - Main dashboard
- `POST /generate_video` - Generate single video
- `POST /generate_multiple` - Generate multiple videos
- `GET /get_videos` - List all videos
- `GET /download_video/<filename>` - Download specific video
- `GET /download_all` - Download all videos as zip
- `POST /start_bot` - Start Instagram bot
- `POST /stop_bot` - Stop Instagram bot
- `GET /bot_status` - Get bot status
- `POST /upload_music` - Upload music file

## Troubleshooting

### Common Issues

1. **Instagram Login Failed**
   - Check your credentials in `config.json`
   - Ensure 2FA is disabled or use app passwords
   - Try logging in manually first

2. **Video Generation Fails**
   - Ensure OpenCV and PIL are installed
   - Check available disk space
   - Verify font files are available

3. **Web Interface Not Loading**
   - Check if Flask is installed: `pip install flask`
   - Ensure port 5000 is not in use
   - Check console for error messages

4. **Ollama Connection Error**
   - Ensure Ollama is running locally
   - Check if the llama3 model is installed
   - Verify the API endpoint is accessible

### Getting Help

- Check the console output for detailed error messages
- Verify all dependencies are installed correctly
- Ensure your Instagram account is not restricted
- Check the CSV file for tracking information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is for educational purposes. Please comply with Instagram's Terms of Service and use responsibly. The authors are not responsible for any account restrictions or bans. 