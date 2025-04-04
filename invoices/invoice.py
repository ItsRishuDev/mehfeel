import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_invoice(invoice_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()

    # Add Invoice Header
    c.setFont("Helvetica-Bold", 26)
    c.drawString(50, height - 50, "Mehfeel Cafe")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 70, "FSSAI : 21422990000209")

    # Business Details
    c.setFont("Helvetica", 10)
    c.drawRightString(550, height - 50, "Main Road, Ghatabillod, Dist. Dhar")
    c.drawRightString(550, height - 65, "PIN: 454773")
    c.drawRightString(550, height - 80, "mehfeelcafe@gmail.com")
    c.drawRightString(550, height - 95, "7987031892, 9171173616")

    # Invoice details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 130, "Bill to:")
    c.setFont("Helvetica", 12)
    c.drawString(90, height - 130, f"{invoice_data.customer_name}")
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, height - 130, invoice_data.invoice_date.strftime("%d/%m/%Y"))

    # Invoice Number
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, f"Invoice ID - {invoice_data.invoice_id}")

    # Table Data
    data = [["S.No", "Item", "Quantity", "Unit Price (₹)", "Total (₹)"]]

    count = 0
    for invoice_item in invoice_data.items.all():
        count += 1
        data.append(
            [
                count,
                invoice_item.item_name_at_purchase,
                invoice_item.quantity,
                f"₹ {invoice_item.item_price_at_purchase:.2f}",
                f"₹ {invoice_item.quantity * invoice_item.item_price_at_purchase:.2f}",
            ]
        )
        for addon_item in invoice_item.item_addons.all():
            count += 1
            data.append(
                [
                    count,
                    addon_item.addon_name_at_purchase,
                    addon_item.quantity,
                    f"₹ {addon_item.addon_price_at_purchase:.2f}",
                    f"₹ {addon_item.quantity * addon_item.addon_price_at_purchase:.2f}",
                ]
            )

    table = Table(data, colWidths=[50, 220, 80, 80, 80])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ]
        )
    )

    table_height = 200 + (count * 20)
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - table_height)

    # Payment Summary
    total_price = invoice_data.total_amount
    c.setFont("Courier", 12)
    c.drawRightString(
        500, height - (table_height + 40), f"Subtotal: ₹ {total_price:.2f}"
    )
    c.drawRightString(500, height - (table_height + 60), "Remaining: ₹ 0.00")
    c.setFont("Courier", 14)
    c.drawRightString(500, height - (table_height + 80), f"Total: ₹ {total_price:.2f}")

    # Payment Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - (table_height + 120), "Payment Details:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - (table_height + 140), "ICICI Bank")
    c.drawString(50, height - (table_height + 155), "Account Name: ESHA JOSHI")
    c.drawString(50, height - (table_height + 170), "Account No.: 409091500790")
    c.drawString(50, height - (table_height + 185), "IFSC: ICIC0004099")

    # Thank You Note
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - (table_height + 230), "THANK YOU FOR YOUR BUSINESS!")

    c.save()
    buffer.seek(0)
    return buffer
