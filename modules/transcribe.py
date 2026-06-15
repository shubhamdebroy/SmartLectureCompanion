from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def transcribe_audio(audio_path):

    with open(audio_path, "rb") as audio_file:

        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="text"
        )

    return transcript