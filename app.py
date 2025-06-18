from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
import time
from datetime import datetime
import threading
from motivation_bot import MotivationBot
import tempfile
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global bot instance
bot = MotivationBot()
bot_running = False
bot_thread = None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/generate_video', methods=['POST'])
def generate_video():
    """Generate a single video with custom quote or random quote"""
    try:
        data = request.get_json()
        custom_quote = data.get('quote', '').strip()
        
        if custom_quote:
            quote = custom_quote
        else:
            # Generate random quote using Ollama
            from motivation_bot import generate_quote_ollama
            quote = generate_quote_ollama()
        
        # Create video
        video_path = bot.create_video(quote)
        
        if video_path and os.path.exists(video_path):
            return jsonify({
                'success': True,
                'message': 'Video generated successfully!',
                'quote': quote,
                'video_path': video_path,
                'filename': os.path.basename(video_path)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate video'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/generate_multiple', methods=['POST'])
def generate_multiple():
    """Generate multiple videos"""
    try:
        data = request.get_json()
        num_videos = int(data.get('count', 5))
        
        if num_videos > 20:  # Limit to prevent abuse
            num_videos = 20
        
        videos = bot.generate_videos_only(num_videos)
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(videos)} videos successfully!',
            'videos': videos
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/download_video/<filename>')
def download_video(filename):
    """Download a specific video file"""
    try:
        video_path = os.path.join(bot.videos_folder, filename)
        if os.path.exists(video_path):
            return send_file(video_path, as_attachment=True)
        else:
            return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_all')
def download_all():
    """Download all generated videos as a zip file"""
    try:
        # Create a temporary zip file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
            for filename in os.listdir(bot.videos_folder):
                if filename.endswith('.mp4'):
                    file_path = os.path.join(bot.videos_folder, filename)
                    zipf.write(file_path, filename)
        
        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name=f'motivation_videos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_videos')
def get_videos():
    """Get list of all generated videos"""
    try:
        videos = []
        if os.path.exists(bot.videos_folder):
            for filename in os.listdir(bot.videos_folder):
                if filename.endswith('.mp4'):
                    file_path = os.path.join(bot.videos_folder, filename)
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    videos.append({
                        'filename': filename,
                        'size_mb': round(file_size, 2),
                        'created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        return jsonify({'videos': videos})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the Instagram posting bot"""
    global bot_running, bot_thread
    
    try:
        if bot_running:
            return jsonify({'success': False, 'message': 'Bot is already running'})
        
        # Check if config exists
        config = bot.load_config()
        if not config or 'instagram' not in config:
            return jsonify({
                'success': False, 
                'message': 'Instagram credentials not found. Please check your config.json file.'
            })
        
        bot_running = True
        bot_thread = threading.Thread(target=run_bot_background)
        bot_thread.daemon = True
        bot_thread.start()
        
        return jsonify({'success': True, 'message': 'Bot started successfully!'})
    
    except Exception as e:
        bot_running = False
        return jsonify({'success': False, 'message': f'Error starting bot: {str(e)}'})

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the Instagram posting bot"""
    global bot_running
    
    try:
        bot_running = False
        return jsonify({'success': True, 'message': 'Bot stopped successfully!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error stopping bot: {str(e)}'})

@app.route('/bot_status')
def bot_status():
    """Get current bot status"""
    return jsonify({'running': bot_running})

@app.route('/upload_music', methods=['POST'])
def upload_music():
    """Upload music files for video generation"""
    try:
        if 'music_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['music_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and file.filename.lower().endswith(('.mp3', '.wav')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(bot.music_folder, filename)
            file.save(file_path)
            
            return jsonify({
                'success': True, 
                'message': f'Music file {filename} uploaded successfully!'
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'Invalid file type. Please upload .mp3 or .wav files only.'
            })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error uploading file: {str(e)}'})

def run_bot_background():
    """Run the bot in background thread"""
    global bot_running
    
    try:
        while bot_running:
            # Get trending quotes
            quotes = bot.get_trending_quotes()
            
            for quote in quotes:
                if not bot_running:
                    break
                
                # Check if quote already exists in CSV
                if not bot.is_quote_posted(quote):
                    # Create video
                    video_path = bot.create_video(quote)
                    if video_path:
                        # Post to Instagram
                        caption = f"💪 {quote}\n\n#motivation #inspiration #success #mindset"
                        posted = bot.post_to_instagram(video_path, caption)
                        
                        # Update CSV
                        bot.update_csv(quote, 'Ollama LLM', posted)
                        
                        # Wait for 1 hour before next post
                        for _ in range(3600):  # 3600 seconds = 1 hour
                            if not bot_running:
                                break
                            time.sleep(1)
            
            # Wait for 6 hours before checking for new trends
            for _ in range(21600):  # 21600 seconds = 6 hours
                if not bot_running:
                    break
                time.sleep(1)
    
    except Exception as e:
        print(f"Error in bot background thread: {e}")
        bot_running = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 