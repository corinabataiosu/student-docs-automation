from pathlib import Path

from request_parser import parse_request
from validator import load_students, validate_request


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"
STUDENTS_FILE = PROJECT_ROOT / "data" / "students.csv"


def main():
    students = load_students(STUDENTS_FILE)

    for request_file in INPUT_DIR.glob("*.txt"):
        print(f"\nProcessing: {request_file.name}")

        try:
            request = parse_request(request_file)
            is_valid, errors = validate_request(request, students)

            if is_valid:
                print(f"VALID: {request['request_id']}")
            else:
                print(f"INVALID: {request['request_id']}")

                for error in errors:
                    print(f"  - {error}")

        except ValueError as error:
            print(f"ERROR: {error}")


if __name__ == "__main__":
    main()