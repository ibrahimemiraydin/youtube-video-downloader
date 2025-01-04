import os
import re

def validate_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
    return re.match(youtube_regex, url) is not None

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
