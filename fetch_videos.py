import os
import yt_dlp
from supabase import create_client, Client

# 1. GitHub Secrets से Supabase का कनेक्शन
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# 2. अपने टीचर्स/चैनल्स के लिंक यहाँ डालें
CHANNEL_URLS = [
    "https://www.youtube.com/@veritasium",  # इसे अपने चैनल लिंक से बदलें
    "https://www.youtube.com/@PhysicsWallah"
]

def fetch_and_update():
    # yt-dlp की सेटिंग्स (हम सिर्फ लेटेस्ट 10 वीडियो ला रहे हैं ताकि फास्ट रहे)
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': '1-10', 
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in CHANNEL_URLS:
            try:
                print(f"Fetching data for: {channel_url}")
                info = ydl.extract_info(channel_url, download=False)
                channel_name = info.get('title', 'Unknown Channel')
                channel_id = info.get('id', 'unknown')
                
                entries = info.get('entries', [])
                for entry in entries:
                    video_id = entry.get('id')
                    title = entry.get('title')
                    
                    # चेक करें कि क्या वीडियो अभी 'LIVE' है
                    live_status = entry.get('live_status')
                    is_live = True if live_status == 'is_live' else False
                    
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    
                    # Supabase में भेजने के लिए डेटा तैयार करना
                    video_data = {
                        "youtube_video_id": video_id,
                        "title": title,
                        "channel_id": channel_name, 
                        "thumbnail_url": thumbnail_url,
                        "is_live": is_live
                    }
                    
                    # डेटाबेस में सेव करना (अगर पहले से है तो अपडेट करेगा)
                    supabase.table('videos').upsert(video_data, on_conflict='youtube_video_id').execute()
                    print(f"Successfully added/updated: {title}")
                    
            except Exception as e:
                print(f"Error fetching {channel_url}: {e}")

if __name__ == "__main__":
    fetch_and_update()
