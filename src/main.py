from pathlib import Path

from request_parser import parse_request
from validator import load_students, validate_request
from processor import process_request

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "data" / "input"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"

STUDENTS_FILE = PROJECT_ROOT / "data" / "students.csv"

def main():
    students = load_students(STUDENTS_FILE)

    process_request(
        input_dir=INPUT_DIR,
        processed_dir=PROCESSED_DIR,
        rejected_dir=REJECTED_DIR,
        students=students
    )


if __name__ == "__main__":
    main()