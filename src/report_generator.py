from pathlib import Path
from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

HEADERS = [
    "Request ID", 
    "Student ID", 
    "Document Type", 
    "Request Date", 
    "Processed at", 
    "Status", 
    "Details"]

def generate_report(report_path: Path, results: list[dict]):

    if report_path.exists():
        workbook = load_workbook(report_path)
        sheet = workbook["Request Report"]
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Request Report"

        sheet.append(HEADERS)

        for cell in sheet[1]:
            cell.font = Font(bold=True)

    existing_request_ids = set()
    for row in sheet.iter_rows(min_row=2, values_only=True):
        request_id = row[0]

        if request_id:
            existing_request_ids.add(request_id)

    processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for result in results:
        request_id = result["request_id"]

        if request_id in existing_request_ids:
            continue

        sheet.append([
            request_id,
            result["student_id"],
            result["document_type"],
            result["request_date"],
            processed_at,
            result["status"],
            result.get("details", ""),
        ])

        existing_request_ids.add(request_id)

    sheet.column_dimensions["A"].width = 10
    sheet.column_dimensions["B"].width = 10
    sheet.column_dimensions["C"].width = 25
    sheet.column_dimensions["D"].width = 15
    sheet.column_dimensions["E"].width = 20
    sheet.column_dimensions["F"].width = 10
    sheet.column_dimensions["G"].width = 50

    report_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(report_path)