import os
import wave
import contextlib


def split_audio(
        audio_path,
        chunk_minutes=10
):
    """
    Split WAV files into smaller WAV chunks.
    Works with Python 3.13.
    No pydub.
    No audiosegment.
    """

    if not audio_path.lower().endswith(".wav"):
        raise ValueError(
            "split_audio() only accepts WAV files."
        )

    os.makedirs(
        "temp",
        exist_ok=True
    )

    chunk_paths = []

    with contextlib.closing(
            wave.open(audio_path, "rb")
    ) as wf:

        frame_rate = wf.getframerate()
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        total_frames = wf.getnframes()

        chunk_frames = (
                chunk_minutes
                * 60
                * frame_rate
        )

        start = 0
        chunk_number = 0

        while start < total_frames:

            wf.setpos(start)

            frames = wf.readframes(
                chunk_frames
            )

            chunk_path = os.path.join(
                "temp",
                f"chunk_{chunk_number}.wav"
            )

            with wave.open(
                    chunk_path,
                    "wb"
            ) as out:

                out.setnchannels(
                    channels
                )

                out.setsampwidth(
                    sample_width
                )

                out.setframerate(
                    frame_rate
                )

                out.writeframes(
                    frames
                )

            chunk_paths.append(
                chunk_path
            )

            start += chunk_frames
            chunk_number += 1

    return chunk_paths