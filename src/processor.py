from pathlib import Path
import shutil

from .request_parser import parse_request
from .validator import validate_request
from .document_generator import generate_document, TEMPLATES

def process_request(
    input_dir: Path,
    processed_dir: Path,
    rejected_dir: Path,
    documents_dir: Path,
    template_path: Path,
    students: dict, 
    logger
):
    logger.info(f"Starting request processing from {input_dir}")
    results = []

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

                document_type = request["document_type"]

                if document_type in TEMPLATES:
                    template = TEMPLATES[document_type]
                    current_template_path = template_path / template

                    document_name = (
                        f"{request['request_id']}_{document_type}.docx"
                    )

                    document_path = documents_dir / document_name

                    generate_document(  
                        template_path=current_template_path,
                        output_path=document_path,
                        student=student,
                        request=request,
                    )

                    logger.info(f"Document generated for request {request['request_id']}: {document_path}")

                    print(f"Document generated: {document_path}")

                destination = processed_dir / request_file.name
                shutil.move(str(request_file), destination)

                results.append({
                "request_id": request["request_id"],
                "student_id": request["student_id"],
                "document_type": request["document_type"],
                "request_date": request["request_date"],
                "status": "Processed",
                "details": f"Document generated: {document_name}",
                })

                logger.info(f"Request {request['request_id']} processed successfully. Moved to: {destination}")

                print(f"VALID: {request['request_id']}")
                print(f"Moved to: {destination}")
            else:
                destination = rejected_dir / request_file.name
                shutil.move(str(request_file), destination)
                
                print(f"INVALID: {request['request_id']}")

                for error in errors:
                    print(f"  - {error}")

                results.append({
                    "request_id": request["request_id"],
                    "student_id": request["student_id"],
                    "document_type": request["document_type"],
                    "request_date": request["request_date"],
                    "status": "Rejected",
                    "details": "; ".join(errors),
                })

                logger.warning(f"Request {request['request_id']} rejected due to validation errors. Moved to: {destination}")

                print(f"Moved to: {destination}")
            
        except ValueError as error:
            destination = rejected_dir / request_file.name
            shutil.move(str(request_file), destination)

            logger.error(f"Error processing request file {request_file.name}: {error}. Moved to: {destination}")
            print(f"ERROR: {error}")
            print(f"Moved to: {destination}")

    logger.info("Request processing completed.")

    return results