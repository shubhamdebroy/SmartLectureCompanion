# Smart Lecture Companion

An AI-powered educational assistant that converts lectures into transcripts, study notes, quizzes, and flashcards using Speech Recognition and Generative AI.

🔗 Live Demo: https://smartlecturecompanion.streamlit.app/

---

## Features

- 🎙️ Automatic Speech-to-Text Transcription
- 📁 Upload Lecture Files (MP3, MP4, WAV, AAC, M4A)
- 🔗 YouTube Lecture Support
- 📝 AI-Generated Study Notes
- ❓ Interactive Quiz Generator
- 🗂️ Flashcards Generator
- 📄 Export Notes as TXT and PDF
- ✂️ Long Lecture Audio Chunking
- 🌐 Professional Streamlit Interface

---

## System Architecture

```text
User
↓
Upload File / YouTube Link
↓
FFmpeg Audio Conversion
↓
Audio Chunking
↓
Groq Whisper Large V3 Turbo
↓
Transcript
↓
Llama 3.3 70B
├── Study Notes
├── Quiz
└── Flashcards
↓
Download TXT/PDF
```

---

## AI Models Used

### 1. Whisper Large V3 Turbo

- **Task:** Speech Recognition (ASR)
- **Provider:** Groq
- **Purpose:** Lecture Transcription

### 2. Llama 3.3 70B Versatile

- **Task:** Generative AI
- **Provider:** Groq
- **Purpose:**
  - Study Notes Generation
  - Quiz Creation
  - Flashcards Creation

---

## Tech Stack

| Component            | Technology                  |
| -------------------- | --------------------------- |
| Frontend             | Streamlit                   |
| Speech-to-Text       | Groq Whisper Large V3 Turbo |
| LLM                  | Llama 3.3 70B Versatile     |
| Audio Conversion     | FFmpeg                      |
| Video Download       | yt-dlp                      |
| PDF Generation       | ReportLab                   |
| Programming Language | Python 3.13                 |

---

## Project Structure

```text
SmartLectureCompanion
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── modules
│   ├── audio_chunker.py
│   ├── audio_utils.py
│   ├── transcribe.py
│   ├── summarizer.py
│   ├── quiz_generator.py
│   ├── flashcards.py
│   ├── youtube_downloader.py
│   └── pdf_generator.py
│
└── temp
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/SmartLectureCompanion.git
cd SmartLectureCompanion
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Project

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Output

✅ Lecture Transcript

✅ AI Study Notes

✅ Interactive Quiz

✅ Flashcards

✅ Downloadable TXT Notes

✅ Downloadable PDF Notes

---

## Future Scope

- Multi-language Lecture Support
- Voice-based Question Answering
- Mind Map Generation
- Automatic PPT Generation
- LMS Integration
- Personalized Revision Planner
- RAG-based Doubt Solving Assistant

---

## Developed By

**Shubham Debroy**

B.Tech Computer Science and Engineering

The Assam Kaziranga University

AI/ML Internship Project – 2026

---

## ⭐ If you found this project useful

Please consider giving the repository a **star ⭐** on GitHub.
