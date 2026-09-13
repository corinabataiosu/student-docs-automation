from pathlib import Path

REQUIRED_FIELDS = {
    "request_id", 
    "student_id", 
    "document_type", 
    "request_date"}

def parse_request(file_path: Path) -> dict:
    request_data = {}

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            key, value = line.split(":", 1)
            request_data[key.strip().lower()] = value.strip()

    missing_fields = REQUIRED_FIELDS - request_data.keys()

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    return request_data