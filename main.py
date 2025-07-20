import yt_dlp

CHANNEL_URL = "https://www.youtube.com/@SyllabuswithRohit/videos"

def get_total_duration(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'dump_single_json': True,
        'playlistend': 500,  # Adjust this limit as needed
        'quiet': True
    }

    print("🔎 Fetching video list...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        video_urls = [entry['url'] for entry in info.get('entries', []) if 'url' in entry]

    print(f"🎬 Found {len(video_urls)} videos. Calculating durations...\n")

    total_seconds = 0
    skipped = 0
    for i, url in enumerate(video_urls, 1):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                video_info = ydl.extract_info(url, download=False)
                duration = video_info.get('duration', 0)
                total_seconds += duration
                print(f"[{i}/{len(video_urls)}] ⏱ {duration // 60:02.0f}m {duration % 60:02.0f}s — {url}")
        except Exception as e:
            skipped += 1
            print(f"[{i}/{len(video_urls)}] ⚠️ Skipping video (reason: {str(e).splitlines()[0][:60]}...)")

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    print("\n✅ Done!")
    print(f"📊 Total Duration: {hours}h {minutes}m {seconds}s")
    print(f"❌ Skipped videos: {skipped}")

if __name__ == "__main__":
    get_total_duration(CHANNEL_URL)
