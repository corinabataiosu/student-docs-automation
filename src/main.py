from pathlib import Path

from request_parser import parse_request
from validator import load_students, validate_request
from processor import process_request
from report_generator import generate_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "data" / "input"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"
DOCUMENTS_DIR = PROJECT_ROOT / "output" / "documents"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
REPORT_FILE = REPORTS_DIR / "request_report.xlsx"

STUDENTS_FILE = PROJECT_ROOT / "data" / "students.csv"
TEMPLATE_DIR = PROJECT_ROOT / "templates" 

def main():
    students = load_students(STUDENTS_FILE)

    results = process_request(
        input_dir=INPUT_DIR,
        processed_dir=PROCESSED_DIR,
        rejected_dir=REJECTED_DIR,
        documents_dir=DOCUMENTS_DIR,
        template_path=TEMPLATE_DIR,
        students=students
    )


    generate_report(REPORT_FILE, results)

    print(f"\nReport generated: {REPORT_FILE}")

if __name__ == "__main__":
    main()