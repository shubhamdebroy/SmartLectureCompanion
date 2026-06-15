import yt_dlp
import os


def download_youtube_audio(url):
    os.makedirs("temp", exist_ok=True)

    output_path = "temp/youtube_audio.%(ext)s"

    ydl_opts = {
        "format": "bestaudio[abr<=64]/bestaudio",
        "outtmpl": output_path,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            url,
            download=True
        )

        file_path = ydl.prepare_filename(info)

    return file_path