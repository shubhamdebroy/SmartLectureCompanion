import streamlit as st
import os

from modules.transcribe import transcribe_audio
from modules.summarizer import generate_summary
from modules.quiz_generator import generate_quiz
from modules.flashcards import generate_flashcards
from modules.youtube_downloader import download_youtube_audio
from modules.audio_chunker import split_audio
from modules.audio_utils import convert_to_wav
from modules.pdf_generator import create_pdf

st.set_page_config(
    page_title="Smart Lecture Companion",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #00D4FF;
}

.stButton>button {
    background-color:#00D4FF;
    color:black;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Smart Lecture Companion")

st.sidebar.markdown("""
### Features

✅ Upload Lecture Files

✅ YouTube Lecture Support

✅ AI Transcription

✅ Study Notes Generation

✅ MCQ Quiz Generator

✅ Flashcards Generator

Built using:
- Groq Whisper
- Llama 3.3 70B
- Streamlit
- yt-dlp
- FFmpeg
""")

st.sidebar.info(
    "YouTube downloads may fail on Streamlit Cloud due to "
    "YouTube restrictions. Uploading lecture files is always supported. To use the YouTube feature, please run the app locally or on a server with unrestricted access."
)

st.title("Smart Lecture Companion")
st.subheader("AI-Powered Voice-to-Notes Generator")

os.makedirs("temp", exist_ok=True)

mode = st.radio(
    "Select Input Mode",
    [
        "📁 Upload Lecture File",
        "🔗 YouTube Lecture Link"
    ],
    horizontal=True
)

uploaded_file = None
youtube_link = ""

if mode == "📁 Upload Lecture File":
    uploaded_file = st.file_uploader(
        "Upload Lecture",
        type=["mp3", "wav", "m4a", "aac", "mp4"]
    )
else:
    youtube_link = st.text_input(
        "Paste YouTube Lecture Link"
    )

if st.button("Generate AI Notes"):

    if mode == "📁 Upload Lecture File" and not uploaded_file:
        st.error("Please upload a lecture file.")
        st.stop()

    if mode == "🔗 YouTube Lecture Link" and not youtube_link:
        st.error("Please paste a YouTube link.")
        st.stop()

    try:
        if mode == "📁 Upload Lecture File":

            save_path = os.path.join(
                "temp",
                uploaded_file.name
            )

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        else:

            with st.spinner(
                " Downloading YouTube Audio..."
            ):

                try:
                    save_path = download_youtube_audio(
                        youtube_link
                    )

                except Exception as e:

                    st.warning(
                        """
⚠️ This YouTube video cannot be downloaded on Streamlit Cloud.

Possible reasons:
• YouTube blocked the cloud server IP
• Private or age-restricted video
• Region-restricted content

Please upload the lecture audio/video file instead.
                        """
                    )

                    st.error(str(e))
                    st.stop()

        with st.spinner(
            " Preparing Audio..."
        ):
            wav_path = convert_to_wav(
                save_path
            )

        with st.spinner(
            " Splitting Audio..."
        ):
            chunks = split_audio(
                wav_path,
                chunk_minutes=10
            )

        transcript = ""

        progress = st.progress(0)

        total = len(chunks)

        for i, chunk in enumerate(chunks):

            text = transcribe_audio(
                chunk
            )

            transcript += text + "\n"

            progress.progress(
                (i + 1) / total
            )

        with st.spinner(
            " Generating Study Notes..."
        ):
            notes = generate_summary(
                transcript
            )

        with st.spinner(
            " Generating Quiz..."
        ):
            quiz = generate_quiz(
                notes
            )

        with st.spinner(
            " Generating Flashcards..."
        ):
            flashcards = generate_flashcards(
                notes
            )

        st.session_state.transcript = transcript
        st.session_state.notes = notes
        st.session_state.quiz = quiz
        st.session_state.flashcards = flashcards

        st.success(
            "✅ Processing Complete!"
        )

    except Exception as e:
        st.error(
            f"Error: {e}"
        )

if "transcript" in st.session_state:

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Transcript",
            "📖 Study Notes",
            "❓ Quiz",
            "🗂 Flashcards"
        ]
    )

    with tab1:

        st.subheader("📝 Transcript")

        st.text_area(
            "Generated Transcript",
            st.session_state.transcript,
            height=400
        )

        st.download_button(
            "⬇ Download Transcript",
            st.session_state.transcript,
            file_name="transcript.txt"
        )

    with tab2:

        st.subheader("📖 Study Notes")

        st.markdown(
            st.session_state.notes
        )

        st.download_button(
            "⬇ Download Notes",
            st.session_state.notes,
            file_name="study_notes.txt"
        )

        pdf = create_pdf(
            st.session_state.notes
        )

        with open(
            pdf,
            "rb"
        ) as f:

            st.download_button(
                "📄 Download PDF Notes",
                f,
                file_name="Study_Notes.pdf"
            )

    with tab3:

        st.subheader("❓ Quiz")

        if isinstance(
            st.session_state.quiz,
            list
        ):

            score = 0
            user_answers = {}

            for i, q in enumerate(
                st.session_state.quiz
            ):

                st.markdown(
                    f"### Q{i+1}. {q['question']}"
                )

                options = []
                option_map = {}

                for key, value in q[
                    "options"
                ].items():

                    text = (
                        f"{key}. {value}"
                    )

                    options.append(
                        text
                    )

                    option_map[
                        text
                    ] = key

                selected = st.radio(
                    "Choose an answer:",
                    options,
                    key=f"q_{i}"
                )

                user_answers[
                    i
                ] = option_map[
                    selected
                ]

            if st.button(
                "Submit Quiz"
            ):

                for i, q in enumerate(
                    st.session_state.quiz
                ):

                    correct = q[
                        "answer"
                    ]

                    user = user_answers[
                        i
                    ]

                    if user == correct:

                        score += 1

                        st.success(
                            f"Q{i+1}: Correct ✅"
                        )

                    else:

                        st.error(
                            f"""
Q{i+1}: Wrong ❌

Your Answer: {user}

Correct Answer: {correct}
"""
                        )

                st.success(
                    f"🎯 Score: {score}/10"
                )

        else:

            st.markdown(
                st.session_state.quiz
            )

    with tab4:

        st.subheader(
            "🗂 Flashcards"
        )

        st.markdown(
            st.session_state.flashcards
        )

        st.download_button(
            "⬇ Download Flashcards",
            st.session_state.flashcards,
            file_name="flashcards.txt"
        )