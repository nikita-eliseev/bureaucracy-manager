from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import date

def generate_cancellation_pdf(contract) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50,
        title="Kündigungsschreiben",
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    small = ParagraphStyle("SmallDE", parent=normal, fontSize=9, textColor=colors.grey)
    address_style = ParagraphStyle("AddressDE", parent=normal, fontSize=10, leading=12)
    subject_style = ParagraphStyle("SubjectDE", parent=normal, fontSize=11, leading=14, textColor=colors.black, spaceAfter=12)
    title_style = ParagraphStyle("TitleDE", parent=styles["Title"], fontSize=16, leading=20, spaceAfter=20)

    elements = []

    # ---------- 1. Absender (links) ----------
    sender_available = all(hasattr(contract, attr) for attr in ['sender_name', 'sender_street', 'sender_plz', 'sender_city'])
    if sender_available:
        sender_lines = [
            contract.sender_name,
            contract.sender_street,
            f"{contract.sender_plz} {contract.sender_city}"
        ]
        sender_text = "<br/>".join(sender_lines)
        elements.append(Paragraph(sender_text, address_style))
        elements.append(Spacer(1, 15))

    # ---------- 2. Empfänger ----------
    receiver_available = hasattr(contract, 'company_name')
    if receiver_available:
        receiver_lines = [contract.company_name]
        if hasattr(contract, 'company_department') and contract.company_department:
            receiver_lines.append(contract.company_department)
        if hasattr(contract, 'company_street') and contract.company_street:
            receiver_lines.append(contract.company_street)
        if hasattr(contract, 'company_plz') and hasattr(contract, 'company_city'):
            receiver_lines.append(f"{contract.company_plz} {contract.company_city}")
        receiver_text = "<br/>".join(receiver_lines)
        elements.append(Paragraph(receiver_text, address_style))
        elements.append(Spacer(1, 20))

    # ---------- 3. Ort und Datum (rechtsbündig) ----------
    if hasattr(contract, 'sender_city') and contract.sender_city:
        city = contract.sender_city
    else:
        city = getattr(contract, 'sender_city', '[Ort]')
    today = date.today().strftime("%d.%m.%Y")
    date_line = f"{city}, den {today}"
    # Tabelle mit einer Zelle für rechtsbündige Ausrichtung
    date_table = Table([[date_line]], colWidths=[doc.width])
    date_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(date_table)
    elements.append(Spacer(1, 12))

    # ---------- 4. Betreff ----------
    subject_text = "Betreff: Kündigung meines Vertrags"
    subject_details = []
    if hasattr(contract, 'customer_number') and contract.customer_number:
        subject_details.append(f"Kundennummer: {contract.customer_number}")
    if hasattr(contract, 'contract_number') and contract.contract_number:
        subject_details.append(f"Vertragsnummer: {contract.contract_number}")
    if subject_details:
        subject_text += f" ({', '.join(subject_details)})"
    elements.append(Paragraph(subject_text, subject_style))
    elements.append(Spacer(1, 15))

    # ---------- 5. Metadaten-Tabelle (optional, aber hilfreich) ----------
    meta_data = []
    if hasattr(contract, 'company_name') and contract.company_name:
        meta_data.append(["Unternehmen", contract.company_name])
    if hasattr(contract, 'contract_type') and contract.contract_type:
        meta_data.append(["Vertragsart", contract.contract_type])
    if hasattr(contract, 'customer_number') and contract.customer_number:
        meta_data.append(["Kundennummer", contract.customer_number])
    if hasattr(contract, 'contract_number') and contract.contract_number:
        meta_data.append(["Vertragsnummer", contract.contract_number])

    if meta_data:
        table = Table(meta_data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

    # ---------- 6. Text des Schreibens ----------
    body = """
    Sehr geehrte Damen und Herren,<br/><br/>
    hiermit kündige ich meinen Vertrag <b>fristgerecht zum nächstmöglichen Zeitpunkt</b>.<br/><br/>
    Bitte bestätigen Sie mir die Kündigung schriftlich unter Angabe des Beendigungszeitpunkts.<br/><br/>
    Sofern eine Einzugsermächtigung bzw. ein SEPA-Lastschriftmandat besteht, widerrufe ich dieses zum Vertragsende.<br/><br/>
    Vielen Dank.<br/><br/>
    Mit freundlichen Grüßen<br/><br/><br/>
    ___________________________<br/>
    """
    # Unterschrift mit wiederholtem Namen des Absenders (falls vorhanden)
    if hasattr(contract, 'sender_name') and contract.sender_name:
        body += f"<b>{contract.sender_name}</b>"
    else:
        body += "(Unterschrift)"
    elements.append(Paragraph(body, normal))
    elements.append(Spacer(1, 25))

    # ---------- 7. Footer ----------
    elements.append(Paragraph(
        "Dieses Dokument wurde automatisch durch den Bürokratie Manager erstellt.",
        small
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer