import pytest
from core.downloader import download_video

def test_download_video():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    try:
        download_video(url)
    except Exception:
        pytest.fail("Download failed")
