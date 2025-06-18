import os
import csv
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from instabot import Bot
import nltk
from nltk.tokenize import sent_tokenize
import time
import json

# Download required NLTK data
nltk.download('punkt')

def generate_quote_ollama():
    prompt = "Generate a short, original motivational quote."
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    if response.status_code == 200:
        try:
            return response.json()['response'].strip()
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Ollama response: {e}")
            return "Success is not final, failure is not fatal: it is the courage to continue that counts."
    else:
        print(f"Error from Ollama API: {response.status_code}")
        return "Success is not final, failure is not fatal: it is the courage to continue that counts."

class MotivationBot:
    def __init__(self):
        self.csv_file = 'motivation_ideas.csv'
        self.config_file = 'config.json'
        self.videos_folder = 'generated_videos'
        self.initialize_csv()
        self.bot = None
        self.music_folder = 'music'
        os.makedirs(self.music_folder, exist_ok=True)
        os.makedirs(self.videos_folder, exist_ok=True)
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.config_file} not found. Please create it with your Instagram credentials.")
            return None
        except json.JSONDecodeError:
            print(f"Error: {self.config_file} is not valid JSON.")
            return None
        
    def initialize_csv(self):
        """Initialize or load the CSV file for tracking ideas"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Idea', 'Source', 'Posted', 'Post_Date'])
        else:
            # Just verify the file exists
            pass
            
    def get_trending_quotes(self):
        """Generate motivational quotes using Ollama LLM"""
        return [generate_quote_ollama() for _ in range(5)]
    
    def get_random_music(self):
        """Get a random music file from the music folder"""
        music_files = [f for f in os.listdir(self.music_folder) if f.endswith(('.mp3', '.wav'))]
        if not music_files:
            return None
        return os.path.join(self.music_folder, random.choice(music_files))
    
    def create_video(self, quote):
        """Create a video with the motivational quote using PIL and OpenCV"""
        try:
            # Video settings
            width, height = 1080, 1920
            fps = 24
            duration = 10  # seconds
            
            # Create a black background
            background = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Create PIL image for text
            img = Image.fromarray(background)
            draw = ImageDraw.Draw(img)
            
            # Load font (use default if custom font not available)
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Wrap text to fit width
            words = quote.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] > width - 100:  # Leave some margin
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            # Calculate text position
            text_height = len(lines) * 70  # Approximate line height
            y = (height - text_height) // 2
            
            # Draw text
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
                y += 70
            
            # Convert PIL image to numpy array
            frame = np.array(img)
            
            # Create video writer
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_quote = "".join(c for c in quote[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            output_path = os.path.join(self.videos_folder, f"motivation_{timestamp}_{safe_quote}.mp4")
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Write frames
            for _ in range(fps * duration):
                out.write(frame)
            
            # Release video writer
            out.release()
            
            print(f"Video saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    def post_to_instagram(self, video_path, caption):
        """Post the video to Instagram"""
        try:
            if not self.bot:
                # Clean up any existing session files
                if os.path.exists("config"):
                    import shutil
                    shutil.rmtree("config")
                
                self.bot = Bot()
                config = self.load_config()
                
                if not config or 'instagram' not in config:
                    print("Error: Instagram credentials not found in config.json")
                    return False
                
                username = config['instagram']['username']
                password = config['instagram']['password']
                
                if not username or not password:
                    print("Error: Instagram credentials not found in config.json")
                    return False
                
                print(f"Logging in to Instagram as {username}...")
                login_success = self.bot.login(username=username, password=password)
                
                if not login_success:
                    print("Failed to log in to Instagram. Please check your credentials.")
                    self.bot = None
                    return False
                
                print("Successfully logged in to Instagram!")
            
            # Verify video file exists and is readable
            if not os.path.exists(video_path):
                print(f"Error: Video file not found at {video_path}")
                return False
                
            # Get video file size
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # Convert to MB
            print(f"Video file size: {file_size:.2f} MB")
            
            if file_size > 100:  # Instagram's limit is 100MB
                print("Error: Video file is too large for Instagram")
                return False
            
            print(f"Uploading video: {video_path}")
            print(f"Caption: {caption}")
            
            # Try to upload with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"Upload attempt {attempt + 1} of {max_retries}")
                    upload_success = self.bot.upload_video(video_path, caption=caption)
                    
                    if upload_success:
                        print("Video upload reported successful!")
                        # Wait a bit to let Instagram process the upload
                        time.sleep(10)
                        
                        # Verify the upload by checking the last media
                        last_media = self.bot.get_last_user_medias(username, 1)
                        if last_media:
                            print("Successfully verified post on Instagram!")
                            return True
                        else:
                            print("Warning: Upload reported successful but post not found on profile")
                            if attempt < max_retries - 1:
                                print("Retrying upload...")
                                continue
                            return False
                    else:
                        print(f"Upload attempt {attempt + 1} failed")
                        if attempt < max_retries - 1:
                            print("Retrying upload...")
                            time.sleep(5)  # Wait before retry
                            continue
                        return False
                        
                except Exception as e:
                    print(f"Error during upload attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        print("Retrying upload...")
                        time.sleep(5)
                        continue
                    raise
            
            return False
            
        except Exception as e:
            print(f"Error posting to Instagram: {e}")
            # Reset bot instance on error
            self.bot = None
            return False
    
    def update_csv(self, idea, source, posted=False):
        """Update the CSV file with new ideas and posting status"""
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d'),
                idea,
                source,
                posted,
                datetime.now().strftime('%Y-%m-%d') if posted else None
            ])
    
    def is_quote_posted(self, quote):
        """Check if a quote has already been posted"""
        if not os.path.exists(self.csv_file):
            return False
        with open(self.csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row[1] == quote:  # Check the 'Idea' column
                    return True
        return False
    
    def run(self):
        """Main function to run the bot"""
        while True:
            try:
                # Get trending quotes
                quotes = self.get_trending_quotes()
                
                for quote in quotes:
                    # Check if quote already exists in CSV
                    if not self.is_quote_posted(quote):
                        # Create video
                        video_path = self.create_video(quote)
                        if video_path:  # Only proceed if video creation was successful
                            # Post to Instagram
                            caption = f"💪 {quote}\n\n#motivation #inspiration #success #mindset"
                            posted = self.post_to_instagram(video_path, caption)
                            
                            # Update CSV
                            self.update_csv(quote, 'Ollama LLM', posted)
                            
                            # Wait for 1 hour before next post
                            time.sleep(3600)
                
                # Wait for 6 hours before checking for new trends
                time.sleep(21600)
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(3600)  # Wait an hour before retrying

    def generate_videos_only(self, num_videos=5):
        """Generate videos without posting to Instagram"""
        print(f"Generating {num_videos} motivational videos...")
        generated_videos = []
        
        for i in range(num_videos):
            quote = generate_quote_ollama()
            print(f"\nGenerating video {i+1}/{num_videos}")
            print(f"Quote: {quote}")
            
            video_path = self.create_video(quote)
            if video_path:
                generated_videos.append({
                    'quote': quote,
                    'video_path': video_path
                })
                print(f"Successfully generated video {i+1}")
            else:
                print(f"Failed to generate video {i+1}")
            
            # Small delay between generations
            time.sleep(1)
        
        print("\nGenerated Videos Summary:")
        for i, video in enumerate(generated_videos, 1):
            print(f"\n{i}. Quote: {video['quote']}")
            print(f"   Video: {video['video_path']}")
        
        return generated_videos

if __name__ == "__main__":
    bot = MotivationBot()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run the full bot (generate and post to Instagram)")
    print("2. Generate videos only (save to folder)")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        bot.run()
    elif choice == "2":
        num_videos = input("How many videos would you like to generate? (default: 5): ")
        try:
            num_videos = int(num_videos) if num_videos.strip() else 5
        except ValueError:
            num_videos = 5
        bot.generate_videos_only(num_videos)
    else:
        print("Invalid choice. Please run the script again and select 1 or 2.") 