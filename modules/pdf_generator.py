from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(text):

    pdf_path = "Study_Notes.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):
        story.append(
            Paragraph(
                line,
                styles["Normal"]
            )
        )

    doc.build(story)

    return pdf_path