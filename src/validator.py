import csv
from pathlib import Path
from datetime import datetime

VALID_DOCUMENT_TYPES = {
    "student_certificate",
    "scholarship_certificate"
}

VALID_STUDENT_STATUSES = {
    "active"
    }

def load_students(file_path: Path) -> dict:
    students = {}

    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            students[row["student_id"]] = row

    return students

def validate_request(request: dict, students: dict) -> tuple[bool, list[str]]:
    errors = []

    # check document type
    if request["document_type"] not in VALID_DOCUMENT_TYPES:
        errors.append(f"Invalid document type: {request['document_type']}")

    # check student ID
    student_id = request["student_id"]

    if student_id not in students:
        errors.append(f"Student ID not found: {student_id}")
    else:
        student = students[student_id]

        if student["enrollment_status"] not in VALID_STUDENT_STATUSES:
            errors.append(f"Invalid student status: {student['enrollment_status']}")

    # check request date
    try:
        datetime.strptime(request["request_date"], "%Y-%m-%d")
    except ValueError:
        errors.append(f"Invalid request date format: {request['request_date']} (expected YYYY-MM-DD)")
        
    return len(errors) == 0, errors