from pathlib import Path

from src.processor import process_request
from src.logger import setup_logger
from src.validator import load_students

def test_process_valid_request(tmp_path: Path):
    input_dir = tmp_path / "input"
    processed_dir = tmp_path / "processed"
    rejected_dir = tmp_path / "rejected"
    documents_dir = tmp_path / "documents"
    templates_dir = tmp_path / "templates"
    students_file = tmp_path / "students.csv"
    log_file = tmp_path / "logs" / "workflow.log"

    input_dir.mkdir()
    templates_dir.mkdir()

    request_file = input_dir / "REQ-TEST-0001.txt"
    request_file.write_text(
        """REQUEST_ID: REQ-TEST-0001
    STUDENT_ID: ST1001
    DOCUMENT_TYPE: student_certificate
    REQUEST_DATE: 2026-06-14
    """,
        encoding="utf-8",
    )

    students_file.write_text(
    """student_id,first_name,last_name,faculty,specialization,year,enrollment_status,email
ST1001,Maria,Popescu,Faculty of Computer Science,Computer Science,3,active,maria@example.com
""",
    encoding="utf-8",
)

    from docx import Document

    template =  Document()
    template.add_paragraph("{{ first_name }} {{ last_name }} - {{ student_id }}")
    template.save(templates_dir / "student_certificate.docx")

    students = load_students(students_file)
    logger = setup_logger(log_file)

    results = process_request(
        input_dir=input_dir,
        processed_dir=processed_dir,
        rejected_dir=rejected_dir,
        documents_dir=documents_dir,
        template_path=templates_dir,
        students=students,
        logger=logger
    )

    assert len(results) == 1
    assert results[0]["status"] == "Processed"

    assert not request_file.exists()
    assert (processed_dir / request_file.name).exists()

    assert (documents_dir / "REQ-TEST-0001_student_certificate.docx").exists()

def test_process_invalid_request(tmp_path: Path):
    input_dir = tmp_path / "input"
    processed_dir = tmp_path / "processed"
    rejected_dir = tmp_path / "rejected"
    documents_dir = tmp_path / "documents"
    templates_dir = tmp_path / "templates"
    students_file = tmp_path / "students.csv"
    log_file = tmp_path / "workflow.log"

    input_dir.mkdir()
    templates_dir.mkdir()

    request_file = input_dir / "REQ-TEST-002.txt"
    request_file.write_text(
        """REQUEST_ID: REQ-TEST-002
    STUDENT_ID: ST9999
    DOCUMENT_TYPE: student_certificate
    REQUEST_DATE: 2026-09-14
    """,
        encoding="utf-8",
    )

    students_file.write_text(
        """student_id,first_name,last_name,faculty,specialization,year,enrollment_status,email
ST1001,Maria,Popescu,Faculty of Computer Science,Computer Science,3,active,maria@example.com
""",
        encoding="utf-8",
    )

    students = load_students(students_file)
    logger = setup_logger(log_file)

    results = process_request(
        input_dir=input_dir,
        processed_dir=processed_dir,
        rejected_dir=rejected_dir,
        documents_dir=documents_dir,
        students=students,
        template_path=templates_dir,
        logger=logger,
    )

    assert len(results) == 1
    assert results[0]["status"] == "Rejected"

    assert not request_file.exists()
    assert (rejected_dir / request_file.name).exists()

    assert not list(documents_dir.glob("*.docx"))