# invoice.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

def create_invoice_pdf(
    pdf_filename,
    invoicing_company,
    kvk,
    vat_nr,
    bank,
    iban,
    bic,
    client_company,
    client_address,
    invoice_number,
    invoice_date,
    expiry_date,
    reference,
    items,
    total_exc,
    total_vat,
    grand_total,
    vat_exempt
):
    """
    Generates a PDF invoice using ReportLab's Platypus.

    Parameters:
        pdf_filename (str): The filename for the generated PDF.
        invoicing_company (str): Name of the invoicing company.
        kvk (str): KVK number.
        vat_nr (str): VAT number.
        bank (str): Bank name.
        iban (str): IBAN number.
        bic (str): BIC number.
        client_company (str): Name of the client company.
        client_address (str): Address of the client company.
        invoice_number (str): Invoice number.
        invoice_date (str): Invoice date in dd-mm-yyyy format.
        expiry_date (str): Expiry date in dd-mm-yyyy format.
        reference (str): Reference for the invoice.
        items (list of dict): List of items, each dict contains 'serial', 'description', 'hours', 'price_exc', 'vat', 'total'.
        total_exc (float): Total price excluding VAT.
        total_vat (float): Total VAT.
        grand_total (float): Grand total including VAT.
        vat_exempt (bool): VAT exemption flag.
    """
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18,
    )
    elements = []
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    # Title
    elements.append(Paragraph("INVOICE", styles["Title"]))
    elements.append(Spacer(1, 12))

    # To Section
    to_info = f"<b>To:</b><br/>{client_company}<br/>{client_address}"
    elements.append(Paragraph(to_info, style_normal))
    elements.append(Spacer(1, 12))

    # Invoicing Company Details
    company_details = (
        f"<b>Invoicing Company:</b> {invoicing_company}<br/>"
        f"<b>KvK nr:</b> {kvk}<br/>"
        f"<b>VAT nr:</b> {vat_nr}<br/>"
        f"<b>Bank:</b> {bank}<br/>"
        f"<b>IBAN:</b> {iban}<br/>"
        f"<b>BIC:</b> {bic}"
    )
    elements.append(Paragraph(company_details, style_normal))
    elements.append(Spacer(1, 12))

    # Invoice Details
    invoice_details = (
        f"<b>Invoice Number:</b> {invoice_number}<br/>"
        f"<b>Invoice Date:</b> {invoice_date}<br/>"
        f"<b>Expiry Date:</b> {expiry_date}<br/>"
        f"<b>Reference:</b> {reference}"
    )
    elements.append(Paragraph(invoice_details, style_normal))
    elements.append(Spacer(1, 24))

    # Items Table
    data = [
        [
            "Sr. No.",
            "Description",
            "Hours",
            "Price Exc.",
            "VAT",
            "Total",
        ]
    ]
    for item in items:
        data.append(
            [
                Paragraph(str(item["serial"]), styles["Normal"]),
                Paragraph(item["description"], styles["Normal"]),
                f"{item['hours']:.2f}",
                f"€{item['price_exc']:.2f}",
                f"€{item['vat']:.2f}",
                f"€{item['total']:.2f}",
            ]
        )

    # Calculate column widths dynamically
    page_width = A4[0] - 60  # Usable width
    colWidths = [0.1 * page_width, 0.4 * page_width, 0.1 * page_width, 0.1 * page_width, 0.1 * page_width, 0.1 * page_width]

    # Create the table
    table = Table(data, colWidths=colWidths)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("WORDWRAP", (0, 0), (-1, -1)),  # Enable word wrapping

        ]
    )
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 12))


    # Totals Table
    totals_data = []
    totals_data.append(["Total Exc.", f"€{total_exc:.2f}"])
    totals_data.append(["Total VAT:", f"€{total_vat:.2f}"])
    totals_data.append(["Grand Total:", f"€{grand_total:.2f}"])

    totals_table = Table(totals_data, colWidths=[250, 150])
    totals_table_style = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]
    )
    totals_table.setStyle(totals_table_style)
    elements.append(totals_table)
    elements.append(Spacer(1, 24))

    # Exemption or Payment Instructions
    if vat_exempt:
        exemption_note = "Invoice exempt from OB based on article 25 OB."
        elements.append(Paragraph(exemption_note, style_normal))
    else:
        payment_instructions = "Please make payment within 30 days to the above account number quoting the invoice number."
        elements.append(Paragraph(payment_instructions, style_normal))

    # Build PDF
    doc.build(elements)
