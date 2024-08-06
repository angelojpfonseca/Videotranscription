import os
import yt_dlp

def is_playlist(url):
    return 'playlist' in url or 'list=' in url

def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'entries' in info:
                # It's a playlist
                for entry in info['entries']:
                    print(f"Downloaded: {entry['title']}")
            else:
                # It's a single video
                print(f"Downloaded: {info['title']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, 'args'):
            print(f"Error args: {e.args}")

def main():
    output_dir = "downloaded_videos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    while True:
        url = input("Enter the YouTube video or playlist URL (or 'q' to quit): ")
        
        if url.lower() == 'q':
            break
        
        if is_playlist(url):
            print("Playlist detected. Downloading all videos...")
        else:
            print("Single video detected.")
        
        download_video(url, output_dir)
        print("Download process completed.")

if __name__ == "__main__":
    main()