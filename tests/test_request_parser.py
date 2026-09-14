from pathlib import Path
import pytest
from src.request_parser import parse_request

def test_parse_request(tmp_path: Path):
    request_file = tmp_path / "request.txt"

    request_file.write_text(
        """REQUEST_ID: REQ-TEST-0001 
        STUDENT_ID: ST1001
        DOCUMENT_TYPE: student_certificate
        REQUEST_DATE: 2026-06-14
        """,
        encoding="utf-8"
    )

    request = parse_request(request_file)

    assert request["request_id"] == "REQ-TEST-0001"
    assert request["student_id"] == "ST1001"
    assert request["document_type"] == "student_certificate"

def test_parse_request_missing_fields(tmp_path: Path):
    request_file = tmp_path / "request.txt"

    request_file.write_text(
        """REQUEST_ID: REQ-TEST-0002 
        STUDENT_ID: ST1002
        DOCUMENT_TYPE: student_certificate
        """,
        encoding="utf-8"
    )

    with pytest.raises(ValueError) as excinfo:
        parse_request(request_file)

    assert "Missing required fields" in str(excinfo.value)
