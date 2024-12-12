import tkinter as tk
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from datetime import datetime, timedelta


class InvoiceApp:
    def __init__(self, master):
        self.master = master
        master.title("Invoice Generator")
        master.geometry("1000x800")  # Adjusted size for better layout

        # Initialize Serial Number Counter
        self.serial_number = 1

        # Scrollable Frame
        self.canvas = tk.Canvas(master)
        self.scroll_y = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # ----- Company and Invoice Details -----

        # Company to be invoiced
        tk.Label(
            self.frame, text="Company to be Invoiced:", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.company_entry = tk.Entry(self.frame, width=60)
        self.company_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)

        # Address
        tk.Label(
            self.frame, text="Address:", font=("Arial", 12, "bold")
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.address_entry = tk.Entry(self.frame, width=60)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

        # KvK nr
        tk.Label(
            self.frame, text="KvK nr:", font=("Arial", 12, "bold")
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.kvk_entry = tk.Entry(self.frame, width=30)
        self.kvk_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # VAT nr
        tk.Label(
            self.frame, text="VAT nr:", font=("Arial", 12, "bold")
        ).grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.vat_entry = tk.Entry(self.frame, width=30)
        self.vat_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)

        # Bank
        tk.Label(
            self.frame, text="Bank:", font=("Arial", 12, "bold")
        ).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.bank_entry = tk.Entry(self.frame, width=30)
        self.bank_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # IBAN
        tk.Label(
            self.frame, text="IBAN:", font=("Arial", 12, "bold")
        ).grid(row=3, column=2, sticky="e", padx=5, pady=5)
        self.iban_entry = tk.Entry(self.frame, width=30)
        self.iban_entry.grid(row=3, column=3, sticky="w", padx=5, pady=5)

        # BIC
        tk.Label(
            self.frame, text="BIC:", font=("Arial", 12, "bold")
        ).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.bic_entry = tk.Entry(self.frame, width=30)
        self.bic_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Invoicing company
        tk.Label(
            self.frame, text="Invoicing Company:", font=("Arial", 12, "bold")
        ).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.invoicing_company_entry = tk.Entry(self.frame, width=60)
        self.invoicing_company_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=3)

        # Invoice details
        tk.Label(
            self.frame, text="Invoice Number:", font=("Arial", 12, "bold")
        ).grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.invoice_number_entry = tk.Entry(self.frame, width=30)
        self.invoice_number_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        tk.Label(
            self.frame, text="Invoice Date (dd-mm-yyyy):", font=("Arial", 12, "bold")
        ).grid(row=6, column=2, sticky="e", padx=5, pady=5)
        self.invoice_date_entry = tk.Entry(self.frame, width=30)
        self.invoice_date_entry.grid(row=6, column=3, sticky="w", padx=5, pady=5)
        self.invoice_date_entry.insert(
            0, datetime.today().strftime("%d-%m-%Y")
        )

        tk.Label(
            self.frame, text="Expiry Date (dd-mm-yyyy):", font=("Arial", 12, "bold")
        ).grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.expiry_date_entry = tk.Entry(self.frame, width=30)
        self.expiry_date_entry.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        default_expiry = datetime.today() + timedelta(days=30)
        self.expiry_date_entry.insert(0, default_expiry.strftime("%d-%m-%Y"))

        tk.Label(
            self.frame, text="Reference:", font=("Arial", 12, "bold")
        ).grid(row=7, column=2, sticky="e", padx=5, pady=5)
        self.reference_entry = tk.Entry(self.frame, width=30)
        self.reference_entry.grid(row=7, column=3, sticky="w", padx=5, pady=5)

        # ----- VAT/OB Exemption -----
        # Initialize vat_exempt before adding item rows
        self.vat_exempt = tk.IntVar()
        self.vat_check = tk.Checkbutton(
            self.frame,
            text="VAT/OB Exemption",
            variable=self.vat_exempt,
            font=("Arial", 12),
            command=self.toggle_vat_exemption,
        )
        self.vat_check.grid(row=8, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        # ----- Items Section -----

        tk.Label(
            self.frame, text="Items", font=("Arial", 14, "bold")
        ).grid(row=9, column=0, columnspan=4, pady=15)

        # Table Headers
        headers = ["Serial Number", "Description", "Hours", "Price Exc.", "VAT", "Total"]
        for idx, header in enumerate(headers):
            tk.Label(
                self.frame,
                text=header,
                borderwidth=1,
                relief="solid",
                width=15,
                bg="lightgrey",
                font=("Arial", 12, "bold"),
            ).grid(row=10, column=idx, padx=1, pady=1)

        self.items_frame = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.items_frame.grid(row=11, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

        self.items = []
        self.add_item_row()

        tk.Button(
            self.frame,
            text="Add Item",
            command=self.add_item_row,
            bg="blue",
            fg="white",
            font=("Arial", 12, "bold"),
        ).grid(row=12, column=0, columnspan=6, pady=10)

        # ----- Generate Button -----

        tk.Button(
            self.frame,
            text="Generate Invoice",
            command=self.generate_invoice,
            bg="green",
            fg="white",
            font=("Arial", 14, "bold"),
        ).grid(row=13, column=0, columnspan=6, pady=20)

    def add_item_row(self):
        row = len(self.items)
        # Define columns: Serial Number, Description, Hours, Price Exc., VAT, Total
        serial_label = tk.Label(self.items_frame, text=str(self.serial_number), width=15, borderwidth=1, relief="solid")
        description = tk.Entry(self.items_frame, width=30)
        hours = tk.Entry(self.items_frame, width=15)
        price_exc = tk.Entry(self.items_frame, width=15)
        vat = tk.Entry(self.items_frame, width=15)
        total = tk.Entry(self.items_frame, width=15, state="readonly")

        serial_label.grid(row=row, column=0, padx=1, pady=1)
        description.grid(row=row, column=1, padx=1, pady=1)
        hours.grid(row=row, column=2, padx=1, pady=1)
        price_exc.grid(row=row, column=3, padx=1, pady=1)
        vat.grid(row=row, column=4, padx=1, pady=1)
        total.grid(row=row, column=5, padx=1, pady=1)

        # Function to calculate Total = Price Exc. + VAT
        def calculate_total(event=None):
            try:
                exc = float(price_exc.get()) if price_exc.get() else 0.0
                vat_val = float(vat.get()) if vat.get() else 0.0
                total_val = exc + vat_val
                total.config(state="normal")
                total.delete(0, tk.END)
                total.insert(0, f"{total_val:.2f}")
                total.config(state="readonly")
            except ValueError:
                total.config(state="normal")
                total.delete(0, tk.END)
                total.insert(0, "0.00")
                total.config(state="readonly")

        # Function to validate Hours input (allow only numeric)
        def validate_hours(event=None):
            value = hours.get()
            if value and not value.replace('.', '', 1).isdigit():
                messagebox.showerror("Invalid Input", "Hours must be a numeric value.")
                hours.delete(0, tk.END)
                hours.insert(0, "0.00")
            calculate_total()

        # Bind events to recalculate total when Price Exc., VAT, or Hours changes
        price_exc.bind("<FocusOut>", calculate_total)
        vat.bind("<FocusOut>", calculate_total)
        hours.bind("<FocusOut>", validate_hours)

        # If VAT exemption is active, set VAT to 0 and disable entry
        if self.vat_exempt.get():
            vat.insert(0, "0.00")
            vat.config(state="readonly")
            calculate_total()

        self.items.append(
            {
                "serial": serial_label,
                "description": description,
                "hours": hours,
                "price_exc": price_exc,
                "vat": vat,
                "total": total,
            }
        )

        # Increment Serial Number Counter
        self.serial_number += 1

    def toggle_vat_exemption(self):
        if self.vat_exempt.get():
            # Set VAT to zero and disable VAT entries
            for item in self.items:
                item["vat"].delete(0, tk.END)
                item["vat"].insert(0, "0.00")
                item["vat"].config(state="readonly")
                # Recalculate total
                item["total"].config(state="normal")
                item["total"].delete(0, tk.END)
                try:
                    exc = float(item["price_exc"].get()) if item["price_exc"].get() else 0.0
                except ValueError:
                    exc = 0.0
                total_val = exc + 0.0
                item["total"].insert(0, f"{total_val:.2f}")
                item["total"].config(state="readonly")
        else:
            # Enable VAT entries
            for item in self.items:
                item["vat"].config(state="normal")
                # Optionally clear VAT fields or keep previous values
                if item["vat"].get() == "0.00":
                    item["vat"].delete(0, tk.END)
                    item["vat"].insert(0, "")
                # Recalculate total if VAT was previously zero
                item["total"].config(state="normal")
                item["total"].delete(0, tk.END)
                try:
                    exc = float(item["price_exc"].get()) if item["price_exc"].get() else 0.0
                    vat_val = float(item["vat"].get()) if item["vat"].get() else 0.0
                except ValueError:
                    exc = vat_val = 0.0
                total_val = exc + vat_val
                item["total"].insert(0, f"{total_val:.2f}")
                item["total"].config(state="readonly")

    def generate_invoice(self):
        try:
            # Collect data
            company = self.company_entry.get().strip()
            address = self.address_entry.get().strip()
            kvk = self.kvk_entry.get().strip()
            vat_nr = self.vat_entry.get().strip()
            bank = self.bank_entry.get().strip()
            iban = self.iban_entry.get().strip()
            bic = self.bic_entry.get().strip()
            invoicing_company = self.invoicing_company_entry.get().strip()
            invoice_number = self.invoice_number_entry.get().strip()
            invoice_date = self.invoice_date_entry.get().strip()
            expiry_date = self.expiry_date_entry.get().strip()
            reference = self.reference_entry.get().strip()
            vat_exempt = self.vat_exempt.get()

            # Validate required fields
            required_fields = [
                company,
                address,
                kvk,
                vat_nr,
                bank,
                iban,
                bic,
                invoicing_company,
                invoice_number,
                invoice_date,
                expiry_date,
            ]
            if not all(required_fields):
                raise ValueError("Please fill in all the required fields.")

            # Validate dates
            try:
                datetime.strptime(invoice_date, "%d-%m-%Y")
                datetime.strptime(expiry_date, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Please enter dates in the format dd-mm-yyyy.")

            # Collect items
            items = []
            for idx, item in enumerate(self.items, start=1):
                description = item["description"].get().strip()
                hours_str = item["hours"].get().strip()
                price_exc_str = item["price_exc"].get().strip()
                vat_str = item["vat"].get().strip()
                total_str = item["total"].get().strip()

                if not all([description, hours_str, price_exc_str, vat_str]):
                    continue  # Skip incomplete rows

                try:
                    hours = float(hours_str)
                    price_exc = float(price_exc_str)
                    vat_val = float(vat_str)
                    total = float(total_str)
                except ValueError:
                    raise ValueError(f"Invalid numeric value in item {idx}.")

                items.append(
                    {
                        "serial": item["serial"].cget("text"),
                        "description": description,
                        "hours": hours,
                        "price_exc": price_exc,
                        "vat": vat_val,
                        "total": total,
                    }
                )

            if not items:
                raise ValueError("Please add at least one valid item.")

            # Calculate totals
            total_exc = sum(item["price_exc"] for item in items)
            total_vat = sum(item["vat"] for item in items) if not vat_exempt else 0.0
            grand_total = total_exc + total_vat

            # Create PDF using Platypus
            pdf_filename = f"Invoice_{invoice_number}.pdf"
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
            style_bold = styles["Heading4"]

            # Title
            elements.append(Paragraph("INVOICE", styles["Title"]))
            elements.append(Spacer(1, 12))

            # To Section
            to_info = f"<b>To:</b><br/>{company}<br/>{address}"
            elements.append(Paragraph(to_info, style_normal))
            elements.append(Spacer(1, 12))

            # Company Details
            company_details = f"""
            <b>KvK nr:</b> {kvk}<br/>
            <b>VAT nr:</b> {vat_nr}<br/>
            <b>Bank:</b> {bank}<br/>
            <b>IBAN:</b> {iban}<br/>
            <b>BIC:</b> {bic}
            """
            elements.append(Paragraph(company_details, style_normal))
            elements.append(Spacer(1, 12))

            # Invoicing Company
            elements.append(
                Paragraph(f"<b>Invoicing Company:</b> {invoicing_company}", style_normal)
            )
            elements.append(Spacer(1, 12))

            # Invoice Details
            invoice_details = f"""
            <b>Invoice Number:</b> {invoice_number}<br/>
            <b>Invoice Date:</b> {invoice_date}<br/>
            <b>Expiry Date:</b> {expiry_date}<br/>
            <b>Reference:</b> {reference}
            """
            elements.append(Paragraph(invoice_details, style_normal))
            elements.append(Spacer(1, 24))

            # Items Table
            data = [["Serial Number", "Description", "Hours", "Price Exc.", "VAT", "Total"]]
            for item in items:
                data.append(
                    [
                        item["serial"],
                        item["description"],
                        f"{item['hours']:.2f}",
                        f"€{item['price_exc']:.2f}",
                        f"€{item['vat']:.2f}",
                        f"€{item['total']:.2f}",
                    ]
                )

            # Define column widths
            table = Table(data, colWidths=[80, 250, 80, 80, 80, 80])
            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                    ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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

            messagebox.showinfo("Success", f"{pdf_filename} has been generated.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
