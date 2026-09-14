from src.validator import validate_request

def test_valid_request():
    students = {
        "ST1001": {
            "student_id": "ST1001",
            "enrollment_status": "active",
        }
    }

    request = {
        "request_id": "REQ-0001",
        "student_id": "ST1001",
        "document_type": "student_certificate",
        "request_date": "2024-06-14",
    }

    is_valid, errors = validate_request(request, students)

    assert is_valid is True
    assert errors == []

def test_unknown_student():
    students = {}

    request = {
        "request_id": "REQ-0002",
        "student_id": "ST9999",
        "document_type": "student_certificate",
        "request_date": "2024-06-14",
    }

    is_valid, errors = validate_request(request, students)

    assert is_valid is False
    assert errors == ["Student ID not found: ST9999"]

def test_inactive_student():
    students = {
        "ST1002": {
            "student_id": "ST1002",
            "enrollment_status": "inactive",
        }
    }

    request = {
        "request_id": "REQ-0003",
        "student_id": "ST1002",
        "document_type": "student_certificate",
        "request_date": "2024-06-14",
    }

    is_valid, errors = validate_request(request, students)

    assert is_valid is False
    assert errors == ["Invalid student status: inactive"]