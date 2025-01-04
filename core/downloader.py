from yt_dlp import YoutubeDL
import re
import os

def download_video(url, quality, output_path, progress_callback):
    # Path to the local FFmpeg binary
    ffmpeg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ffmpeg', 'bin', 'ffmpeg.exe')
    
    # Ensure the path is correct
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"FFmpeg executable not found at {ffmpeg_path}")
    
    
    # Map quality options to yt-dlp format strings
    quality_map = {
        "Highest Quality": "bestvideo+bestaudio",
        "2160p": "bestvideo[height<=2160]+bestaudio",
        "1440p": "bestvideo[height<=1440]+bestaudio",
        "1080p": "bestvideo[height<=1080]+bestaudio",
        "720p": "bestvideo[height<=720]+bestaudio",
        "480p": "bestvideo[height<=480]+bestaudio",
        "360p": "bestvideo[height<=360]+bestaudio",
        "240p": "bestvideo[height<=240]+bestaudio",
        "144p": "bestvideo[height<=144]+bestaudio",
        "Audio Only": "bestaudio"
    }

    # Use yt-dlp options
    ydl_opts = {
        'format': quality_map[quality],  # Select format based on user choice
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Set output template
        'progress_hooks': [lambda d: progress_hook(d, progress_callback)],  # Track progress
        'noplaylist': True,  # Don't download playlists
        'quiet': False,  # Enable output to debug any issues
        'merge_output_format': 'mp4',  # Ensure the output is a standard video format
        'ffmpeg_location': ffmpeg_path,  # Point to the local ffmpeg
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # Start the download

def progress_hook(data, progress_callback):
    if data['status'] == 'downloading':
        percent_str = data.get('_percent_str', '0.0').strip()
        # Remove color codes and other non-numeric characters
        percent_cleaned = re.sub(r'[^\d.]', '', percent_str)
        try:
            percent = float(percent_cleaned)
            progress_callback(percent)
        except ValueError:
            pass  # Ignore invalid percentage strings
