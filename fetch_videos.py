import os
import json
from datetime import datetime
import yt_dlp

# --- Configuration ---
# Apne manpasand 5 educational channels ke URLs yahan dalein
CHANNEL_URLS = [
    "https://www.youtube.com/@3blue1brown",
    "https://www.youtube.com/@Kurzgesagt",
    "https://www.youtube.com/@Veritasium",
    "https://www.youtube.com/@CrashCourse",
    "https://www.youtube.com/@TEDEd"
]

JSON_FILENAME = "videos.json"
MAX_VIDEOS_LIMIT = 2000
MIN_DURATION_SECONDS = 180  # 3 minutes (Shorts ko ignore karne ke liye)

def load_existing_videos(filename):
    """Pehle se maujood videos.json file ko load karta hai."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            print(f"Warning: {filename} kharab thi. Nayi file banayi ja rahi hai.")
            return []
    return []

def save_videos(filename, videos):
    """Videos data ko JSON file me save karta hai."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)

def fetch_latest_videos(channel_urls):
    """yt-dlp ka use karke har channel se latest 5 valid videos nikalta hai."""
    # Speed tez karne aur sirf metadata nikalne ke liye options
    ydl_opts = {
        'extract_flat': False,      # Duration check karne ke liye zaroori hai
        'skip_download': True,      # Video download nahi karni, sirf data chahiye
        'playlistend': 12,          # Top 12 videos dekhega taaki agar beech me Shorts ho toh skip karke 5 long videos mil sakein
        'quiet': True,
        'no_warnings': True,
    }
    
    fetched_videos = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in channel_urls:
            print(f"Channel process ho raha hai: {url}")
            try:
                channel_info = ydl.extract_info(url, download=False)
                
                if not channel_info or 'entries' not in channel_info:
                    print(f"Is channel par koi video nahi mili: {url}")
                    continue
                
                channel_name = channel_info.get('title') or channel_info.get('uploader', 'Unknown Channel')
                valid_videos_count = 0
                
                for entry in channel_info['entries']:
                    if not entry:
                        continue
                    
                    # 1. Shorts filter: Agar video 3 min (180s) se choti hai toh skip karein
                    duration = entry.get('duration')
                    if duration is None or duration < MIN_DURATION_SECONDS:
                        continue
                    
                    # 2. Required data extract karein
                    video_id = entry.get('id')
                    title = entry.get('title')
                    
                    # Thumbnail nikalne ke liye safely check karein
                    thumbnails = entry.get('thumbnails', [])
                    thumbnail_url = thumbnails[-1]['url'] if thumbnails else None
                    
                    # Sorting ke liye date format set karein
                    upload_date_str = entry.get('upload_date')
                    if upload_date_str:
                        try:
                            fetched_at = datetime.strptime(upload_date_str, "%Y%m%d").isoformat()
                        except ValueError:
                            fetched_at = datetime.utcnow().isoformat()
                    else:
                        fetched_at = datetime.utcnow().isoformat()
                    
                    video_data = {
                        "video_id": video_id,
                        "title": title,
                        "thumbnail_url": thumbnail_url,
                        "channel_name": channel_name,
                        "fetched_at": fetched_at
                    }
                    
                    fetched_videos.append(video_data)
                    valid_videos_count += 1
                    
                    # Jaise hi 5 lambi videos mil jayein, is channel ka loop rok dein
                    if valid_videos_count >= 5:
                        break
                        
                print(f"-> Is channel se {valid_videos_count} valid videos mili.")
                
            except Exception as e:
                print(f"Error {url}: {e}")
                
    return fetched_videos

def main():
    # 1. Purana data load karein
    existing_videos = load_existing_videos(JSON_FILENAME)
    existing_ids = {v['video_id'] for v in existing_videos}
    
    # 2. Naya data fetch karein
    print("yt-dlp se data nikala ja raha hai...")
    new_videos = fetch_latest_videos(CHANNEL_URLS)
    
    # 3. Duplicate check karke sirf nayi videos append karein
    added_count = 0
    for video in new_videos:
        if video['video_id'] not in existing_ids:
            existing_videos.append(video)
            existing_ids.add(video['video_id'])
            added_count += 1
            
    print(f"{added_count} nayi unique videos mili aur add ki gayi.")
    
    # 4. Saari videos ko date ke hisab se sort karein (Newest first)
    existing_videos.sort(key=lambda x: x.get('fetched_at', ''), reverse=True)
    
    # 5. Strict 2000 Limit check: Agar zyada hain toh purani videos delete karein
    if len(existing_videos) > MAX_VIDEOS_LIMIT:
        removed_count = len(existing_videos) - MAX_VIDEOS_LIMIT
        existing_videos = existing_videos[:MAX_VIDEOS_LIMIT]
        print(f"Limit cross ho gayi thi! {removed_count} sabse purani videos hata di gayi hain.")
        
    # 6. JSON file me vapas save karein
    save_videos(JSON_FILENAME, existing_videos)
    print(f"Data successfully sync ho gaya. Total videos count: {len(existing_videos)}")

if __name__ == "__main__":
    main()
