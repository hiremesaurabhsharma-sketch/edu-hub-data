import os
import yt_dlp
from supabase import create_client, Client

# Supabase Credentials
url: str = "https://sysxryxguqjjwqdydmkd.supabase.co"
key: str = "sb_publishable_zJsY2l-NP38i15X8QymP7A_J2kUzbbb"
supabase: Client = create_client(url, key)

# आपके सभी चैनल्स की लिस्ट
CHANNEL_URLS = [
    # --- UPSC / IAS ---
    "https://www.youtube.com/@PWOnlyIAS",
    "https://www.youtube.com/@SleepyClasses",
    "https://www.youtube.com/@insightsiasofficial",
    "https://www.youtube.com/@BYJUSIAS",
    "https://www.youtube.com/@ForumIASOfficial",
    "https://www.youtube.com/@iasbaba-official",
    "https://www.youtube.com/@StudyIQIASHindi",
    "https://www.youtube.com/@CivilsDailyIAS",
    "https://www.youtube.com/@UnacademyUPSCCSE",
    "https://www.youtube.com/@ChahalAcademy",
    "https://www.youtube.com/@MalukaIAS",
    "https://www.youtube.com/@KSGIndia",
    "https://www.youtube.com/@ShankarIASAcademy",
    "https://www.youtube.com/@EliteIAS",
    "https://www.youtube.com/@VajiramandRaviOfficial",
    "https://www.youtube.com/@KhanGlobalStudies",
    "https://www.youtube.com/@LukmaanIAS",
    "https://www.youtube.com/@Edukemy",
    "https://www.youtube.com/@AnalystIAS",
    "https://www.youtube.com/@TathastuICS",
    "https://www.youtube.com/@ALSIASOfficial",
    "https://www.youtube.com/@ChronicleIAS",
    "https://www.youtube.com/@GSSCOREofficial",
    "https://www.youtube.com/@DhyeyaIASHindi",
    "https://www.youtube.com/@SriramsIAS",

    # --- SSC / CGL / Govt Exams ---
    "https://www.youtube.com/@RojgarwithAnkit",
    "https://www.youtube.com/@KDLIVE",
    "https://www.youtube.com/@wifistudy",
    "https://www.youtube.com/@SSCMaker",
    "https://www.youtube.com/@RamoMaths",
    "https://www.youtube.com/@ssccglpinnacle",
    "https://www.youtube.com/@TestbookSSC",
    "https://www.youtube.com/@MDClasses",
    "https://www.youtube.com/@EnglishWithJaideepSir",
    "https://www.youtube.com/@LearnWithAmanAndBarkha",
    "https://www.youtube.com/@ReasoningByPiyushVarshney",
    "https://www.youtube.com/@MathsBySahilSir",
    "https://www.youtube.com/@NEONCLASSES",
    "https://www.youtube.com/@e1coachingcenter",
    "https://www.youtube.com/@MathsByArunSir",
    "https://www.youtube.com/@SSCAdda247",
    "https://www.youtube.com/@SSCExampur",
    "https://www.youtube.com/@SuperSuperSSC",
    "https://www.youtube.com/@GaganPratapTalks",
    "https://www.youtube.com/@EnglishWithGopalVerma",
    "https://www.youtube.com/@ReasoningByDeepakSir",
    "https://www.youtube.com/@AdityaRanjanTalks",
    "https://www.youtube.com/@CareerwillExams",
    "https://www.youtube.com/@SChandAcademy",
    "https://www.youtube.com/@TopersPrimeSSC",

    # --- JEE Main & Advanced ---
    "https://www.youtube.com/@JEEWallah",
    "https://www.youtube.com/@MotionIITJEE",
    "https://www.youtube.com/@UnacademyAtoms",
    "https://www.youtube.com/@ApniKakshaJEE",
    "https://www.youtube.com/@ATPSTARJEE",
    "https://www.youtube.com/@EtoosEducation",
    "https://www.youtube.com/@ALLENJEE",
    "https://www.youtube.com/@VedantuJEEEnglish",
    "https://www.youtube.com/@SriChaitanyaEducationalInstitutions",
    "https://www.youtube.com/@IITianExplains",
    "https://www.youtube.com/@VineetLoomba",
    "https://www.youtube.com/@namokaul",
    "https://www.youtube.com/@sachinsirphysics",
    "https://www.youtube.com/@arvindkalia",
    "https://www.youtube.com/@DexterChem",
    "https://www.youtube.com/@VoraClasses",
    "https://www.youtube.com/@PhysicsGalaxyOfficial",
    "https://www.youtube.com/@UnacademyJEEEnglish",
    "https://www.youtube.com/@ResonanceEdu",
    "https://www.youtube.com/@FIITJEEOfficial",
    "https://www.youtube.com/@NarayanaEducationalInstitutions",
    "https://www.youtube.com/@CanvasClasses",
    "https://www.youtube.com/@MKASirIITianExplains",
    "https://www.youtube.com/@PhysicsbyNKCSir",
    "https://www.youtube.com/@Mathsmerizing",

    # --- NEET / Medical ---
    "https://www.youtube.com/@NEETWallahPW",
    "https://www.youtube.com/@CompetitionWallah",
    "https://www.youtube.com/@AakashNEET",
    "https://www.youtube.com/@DrAnandMani",
    "https://www.youtube.com/@GarimaGoelBiology",
    "https://www.youtube.com/@SeepPahuja",
    "https://www.youtube.com/@RituRattewal",
    "https://www.youtube.com/@BiomentorsClassesOnline",
    "https://www.youtube.com/@VedantuNEET",
    "https://www.youtube.com/@OzoneClasses",
    "https://www.youtube.com/@BeWiseClasses",
    "https://www.youtube.com/@Physicsaholics",
    "https://www.youtube.com/@TamannaChaudhary",
    "https://www.youtube.com/@KVEDUCATION",
    "https://www.youtube.com/@NeelaBakoreTutorials",
    "https://www.youtube.com/@UnacademyNEETEnglish",
    "https://www.youtube.com/@PWEnglishNEET",
    "https://www.youtube.com/@NEETprep",
    "https://www.youtube.com/@BiologybyAmritSir",
    "https://www.youtube.com/@NewLightInstitute",
    "https://www.youtube.com/@CommandOnBiology",
    "https://www.youtube.com/@SinghSirChemistry",
    "https://www.youtube.com/@DrSKSingh",
    "https://www.youtube.com/@ShipraMishra",
    "https://www.youtube.com/@GoalNEET"
]

def fetch_and_update():
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': '1-50', # 50 वीडियोस कर दिया गया है
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in CHANNEL_URLS:
            # Shorts को हटाने के लिए '/videos' टैब का इस्तेमाल
            video_tab_url = channel_url + "/videos"
            try:
                print(f"Fetching data for: {video_tab_url}")
                info = ydl.extract_info(video_tab_url, download=False)
                channel_name = info.get('title', 'Unknown Channel')
                
                entries = info.get('entries', [])
                for entry in entries:
                    video_id = entry.get('id')
                    
                    # --- नया फ़िल्टर: चैनल ID (UC...) और गलत ID को ब्लॉक करना ---
                    if not video_id or video_id.startswith('UC') or len(video_id) != 11:
                        continue
                    # ----------------------------------------------------------
                    
                    title = entry.get('title')
                    
                    live_status = entry.get('live_status')
                    is_live = True if live_status == 'is_live' else False
                    
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    
                    video_data = {
                        "youtube_video_id": video_id,
                        "title": title,
                        "channel_id": channel_name, 
                        "thumbnail_url": thumbnail_url,
                        "is_live": is_live
                    }
                    
                    supabase.table('videos').upsert(video_data, on_conflict='youtube_video_id').execute()
                    print(f"Successfully added/updated: {title}")
                    
            except Exception as e:
                print(f"Error fetching {video_tab_url}: {e}")

if __name__ == "__main__":
    fetch_and_update()
