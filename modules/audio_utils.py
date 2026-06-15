import os
import subprocess


def convert_to_wav(input_path):
    """
    Converts MP3, MP4, AAC, M4A, WebM etc.
    into WAV format.

    Returns:
        Path to converted WAV file
    """

    os.makedirs("temp", exist_ok=True)

    filename = os.path.splitext(
        os.path.basename(input_path)
    )[0]

    output_path = os.path.join(
        "temp",
        f"{filename}.wav"
    )

    if input_path.lower().endswith(".wav"):
        return input_path

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        output_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return output_path