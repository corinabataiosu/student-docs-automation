from pathlib import Path

from request_parser import parse_request
from validator import load_students, validate_request
from processor import process_request

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "data" / "input"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"
DOCUMENTS_DIR = PROJECT_ROOT / "output" / "documents"

STUDENTS_FILE = PROJECT_ROOT / "data" / "students.csv"
TEMPLATE_FILE = PROJECT_ROOT / "templates" / "student_certificate.docx"

def main():
    students = load_students(STUDENTS_FILE)

    process_request(
        input_dir=INPUT_DIR,
        processed_dir=PROCESSED_DIR,
        rejected_dir=REJECTED_DIR,
        documents_dir=DOCUMENTS_DIR,
        template_path=TEMPLATE_FILE,
        students=students
    )

if __name__ == "__main__":
    main()