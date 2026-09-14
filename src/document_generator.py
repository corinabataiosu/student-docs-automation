from pathlib import Path

from docx import Document

def generate_student_certificate(
    template_path: Path,
    output_path: Path,
    student: dict,
    request: dict,
):
    document = Document(template_path)

    replacements = {
        "{{ first_name }}": student["first_name"],
        "{{ last_name }}": student["last_name"],
        "{{ student_id }}": student["student_id"],
        "{{ faculty }}": student["faculty"],
        "{{ specialization }}": student["specialization"],
        "{{ year }}": student["year"],
        "{{ enrollment_status }}": student["enrollment_status"],
        "{{ request_id }}": request["request_id"],
        "{{ request_date }}": request["request_date"],
    }

    for paragraph in document.paragraphs:
        for old_text, new_text in replacements.items():
            if old_text in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(old_text, new_text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)