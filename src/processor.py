from pathlib import Path
import shutil

from request_parser import parse_request
from validator import validate_request
from document_generator import generate_student_certificate

def process_request(
    input_dir: Path,
    processed_dir: Path,
    rejected_dir: Path,
    documents_dir: Path,
    template_path: Path,
    students: dict
):
    processed_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)
    documents_dir.mkdir(parents=True, exist_ok=True)

    for request_file in input_dir.glob("*.txt"):
        print(f"\nProcessing: {request_file.name}")

        try:
            request = parse_request(request_file)
            is_valid, errors = validate_request(request, students)

            if is_valid:
                student = students[request["student_id"]]

                if request["document_type"] == "student_certificate":
                    document_name = (f"{request['request_id']}_student_certificate.docx")

                    document_path = documents_dir / document_name

                    generate_student_certificate(  
                        template_path=template_path,
                        output_path=document_path,
                        student=student,
                        request=request,
                    )

                    print(f"Document generated: {document_path}")

                destination = processed_dir / request_file.name
                shutil.move(str(request_file), destination)

                print(f"VALID: {request['request_id']}")
                print(f"Moved to: {destination}")
            else:
                destination = rejected_dir / request_file.name
                shutil.move(str(request_file), destination)
                
                print(f"INVALID: {request['request_id']}")

                for error in errors:
                    print(f"  - {error}")

                print(f"Moved to: {destination}")

        except ValueError as error:
            destination = rejected_dir / request_file.name
            shutil.move(str(request_file), destination)

            print(f"ERROR: {error}")
            print(f"Moved to: {destination}")