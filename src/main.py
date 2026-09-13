from pathlib import Path

from request_parser import parse_request


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"


def main():
    request_file = INPUT_DIR / "REQ-0001.txt"

    request = parse_request(request_file)

    print("University Secretariat Workflow Automation")
    print(request)


if __name__ == "__main__":
    main()