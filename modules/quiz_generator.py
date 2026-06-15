from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_quiz(notes):

    prompt = f"""
Generate exactly 10 multiple-choice questions.

Return ONLY valid JSON.

Example:

[
  {{
    "question":"What is AI?",
    "options":
    {{
      "A":"Option A",
      "B":"Option B",
      "C":"Option C",
      "D":"Option D"
    }},
    "answer":"B"
  }}
]

Notes:
{notes}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    quiz_text = response.choices[0].message.content.strip()


    quiz_text = quiz_text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    try:
        return json.loads(quiz_text)

    except Exception as e:
        print(e)
        return []