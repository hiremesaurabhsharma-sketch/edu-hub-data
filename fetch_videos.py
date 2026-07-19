import json
import os
import yt_dlp

# 1. आपके टॉप 5 एजुकेशनल चैनल्स की लिस्ट
CHANNEL_URLS = [
    "https://www.youtube.com/@PhysicsWallah",
    "https://www.youtube.com/@khanacademy",
    "https://www.youtube.com/@TEDEd",
    "https://www.youtube.com/@crashcourse",
    "https://www.youtube.com/@veritasium"
]

JSON_FILENAME = "videos.json"
MAX_VIDEOS = 2000

def fetch_channel_videos():
    # yt-dlp की सेटिंग (ताकि यह तेजी से काम करे और सिर्फ डेटा लाए)
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlist_items': '1-15', # हम 15 वीडियो चेक करेंगे ताकि Shorts हटने के बाद 5 मिल जाएं
        'quiet': True,
    }

    new_videos = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in CHANNEL_URLS:
            try:
                print(f"Fetching data for: {url}")
                info = ydl.extract_info(url, download=False)
                channel_name = info.get('uploader') or info.get('title') or "Unknown Channel"
                
                entries = info.get('entries', [])
                valid_videos_found = 0
                
                for entry in entries:
                    if valid_videos_found >= 5:
                        break # जैसे ही 5 सही वीडियो मिल जाएं, रुक जाओ
                        
                    duration = entry.get('duration')
                    
                    # 3 मिनट (180 सेकंड) से छोटे वीडियो (यानी Shorts) को इग्नोर करें
                    if duration and duration >= 180:
                        video_data = {
                            "title": entry.get('title'),
                            "video_id": entry.get('id'),
                            "thumbnail_url": f"https://i.ytimg.com/vi/{entry.get('id')}/hqdefault.jpg",
                            "channel_name": channel_name
                        }
                        new_videos.append(video_data)
                        valid_videos_found += 1
                        
            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return new_videos

def update_json(new_videos):
    existing_videos = []
    
    # पुरानी फाइल पढ़ें (अगर मौजूद है)
    if os.path.exists(JSON_FILENAME):
        try:
            with open(JSON_FILENAME, 'r', encoding='utf-8') as f:
                existing_videos = json.load(f)
        except json.JSONDecodeError:
            existing_videos = []

    # डुप्लीकेट चेक करने के लिए मौजूदा video_id की लिस्ट बनाएं
    existing_ids = {vid['video_id'] for vid in existing_videos}
    
    # नए वीडियो जोड़ें (नए वीडियो सबसे ऊपर आएंगे)
    added_count = 0
    for vid in new_videos:
        if vid['video_id'] not in existing_ids:
            existing_videos.insert(0, vid)
            added_count += 1

    # 2000 वीडियो की लिमिट (ताकि वेबसाइट कभी स्लो न हो)
    if len(existing_videos) > MAX_VIDEOS:
        existing_videos = existing_videos[:MAX_VIDEOS]

    # फाइल को वापस सुरक्षित रूप से सेव करें
    with open(JSON_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(existing_videos, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully added {added_count} new videos. Total videos in database: {len(existing_videos)}")

if __name__ == "__main__":
    print("Starting video fetch process...")
    videos = fetch_channel_videos()
    update_json(videos)
    print("Process completed!")
