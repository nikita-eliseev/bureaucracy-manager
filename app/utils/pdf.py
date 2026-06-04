from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_contract_pdf(contract) -> BytesIO:
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Helvetica", 12)

    p.drawString(100, 800, f"Contract ID: {contract.id}")
    p.drawString(100, 780, f"Company: {contract.company}")
    p.drawString(100, 760, f"Type: {contract.contract_type}")
    p.drawString(100, 740, f"End date: {contract.end_date}")
    p.drawString(100, 720, f"Cancellation deadline: {contract.cancellation_deadline}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer