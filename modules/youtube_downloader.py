import os
import yt_dlp


def download_youtube_audio(url):
    """
    Downloads YouTube audio and returns the local file path.
    Works locally and on Streamlit Cloud for public videos, but note that
    some videos may still be blocked by YouTube (HTTP 403) depending on
    YouTube restrictions or cloud IP bans.
    """
    os.makedirs("temp", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": "temp/youtube_audio.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36"
            )
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            downloaded_file = ydl.prepare_filename(info)

            if not os.path.exists(downloaded_file):
                base = os.path.splitext(downloaded_file)[0]
                for ext in ["m4a", "webm", "mp3", "opus"]:
                    candidate = f"{base}.{ext}"
                    if os.path.exists(candidate):
                        downloaded_file = candidate
                        break

            return downloaded_file

    except Exception as e:
        raise RuntimeError(f"YouTube download failed: {e}")
