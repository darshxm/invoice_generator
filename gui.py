# gui.py

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from database import Database
from utils import is_float
from invoice import create_invoice_pdf

class InvoiceApp:
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style("cosmo")  # Use a modern theme
        master.title("Invoice Generator")
        master.geometry("1200x800")

        # Initialize Database
        self.db = Database()

        # Initialize Serial Number Counter
        self.serial_number = 1

        # Scrollable Frame
        self.canvas = ttk.Canvas(master)
        self.scroll_y = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview, bootstyle=SECONDARY)
        self.frame = ttk.Frame(self.canvas)

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

        # ----- Invoicing Company Selection and Management -----
        ttk.Label(
            self.frame, text="Invoicing Company:", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.invoicing_company_var = ttk.StringVar()
        self.invoicing_company_combo = ttk.Combobox(
            self.frame,
            textvariable=self.invoicing_company_var,
            state="readonly",
            width=50,
            bootstyle=INFO
        )
        self.invoicing_company_combo['values'] = self.db.get_invoicing_companies()
        self.invoicing_company_combo.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.invoicing_company_combo.bind("<<ComboboxSelected>>", self.populate_invoicing_company_details)

        ttk.Button(
            self.frame,
            text="Add Invoicing Company",
            command=self.add_invoicing_company,
            bootstyle=(PRIMARY, OUTLINE)
        ).grid(row=0, column=3, padx=5, pady=5)

        # Invoicing Company Details
        ttk.Label(
            self.frame, text="KVK nr:", font=("Arial", 12, "bold")
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.kvk_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.kvk_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(
            self.frame, text="VAT nr:", font=("Arial", 12, "bold")
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.vat_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.vat_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(
            self.frame, text="Bank:", font=("Arial", 12, "bold")
        ).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.bank_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.bank_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(
            self.frame, text="IBAN:", font=("Arial", 12, "bold")
        ).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.iban_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.iban_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(
            self.frame, text="BIC:", font=("Arial", 12, "bold")
        ).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.bic_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.bic_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2)
        
        # Edit Invoicing Company
        ttk.Button(
            self.frame,
            text="Edit Invoicing Company",
            command=self.edit_invoicing_company,
            bootstyle=(INFO, OUTLINE)
        ).grid(row=0, column=4, padx=5, pady=5)        

        # ----- Client Selection and Management -----
        ttk.Label(
            self.frame, text="Client Company:", font=("Arial", 12, "bold")
        ).grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.client_company_var = ttk.StringVar()
        self.client_company_combo = ttk.Combobox(
            self.frame,
            textvariable=self.client_company_var,
            state="readonly",
            width=50,
            bootstyle=INFO
        )
        self.client_company_combo['values'] = self.db.get_clients()
        self.client_company_combo.grid(row=6, column=1, padx=5, pady=5, columnspan=2)
        self.client_company_combo.bind("<<ComboboxSelected>>", self.populate_client_company_details)

        ttk.Button(
            self.frame,
            text="Add Client Company",
            command=self.add_client_company,
            bootstyle=(PRIMARY, OUTLINE)
        ).grid(row=6, column=3, padx=5, pady=5)

        ttk.Label(
            self.frame, text="Address:", font=("Arial", 12, "bold")
        ).grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.client_address_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.client_address_entry.grid(row=7, column=1, padx=5, pady=5, columnspan=2)       

        # Edit Client Company
        ttk.Button(
            self.frame,
            text="Edit Client Company",
            command=self.edit_client_company,
            bootstyle=(INFO, OUTLINE)
        ).grid(row=6, column=4, padx=5, pady=5)


        # ----- Invoice Metadata -----
        ttk.Label(
            self.frame, text="Invoice Number:", font=("Arial", 12, "bold")
        ).grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.invoice_number_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.invoice_number_entry.grid(row=8, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(
            self.frame,
            text="Invoice Date (dd-mm-yyyy):",
            font=("Arial", 12, "bold")
        ).grid(row=9, column=0, sticky="e", padx=5, pady=5)
        self.invoice_date_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.invoice_date_entry.grid(row=9, column=1, padx=5, pady=5, columnspan=2)
        self.invoice_date_entry.insert(0, datetime.today().strftime("%d-%m-%Y"))

        ttk.Label(
            self.frame,
            text="Expiry Date (dd-mm-yyyy):",
            font=("Arial", 12, "bold")
        ).grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.expiry_date_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.expiry_date_entry.grid(row=10, column=1, padx=5, pady=5, columnspan=2)
        default_expiry = datetime.today() + timedelta(days=30)
        self.expiry_date_entry.insert(0, default_expiry.strftime("%d-%m-%Y"))
        
        ttk.Label(
            self.frame, text="Reference:", font=("Arial", 12, "bold")
        ).grid(row=11, column=0, sticky="e", padx=5, pady=5)
        self.reference_entry = ttk.Entry(self.frame, width=50, bootstyle=INFO)
        self.reference_entry.grid(row=11, column=1, padx=5, pady=5, columnspan=2)

        self.vat_exempt = ttk.IntVar()
        self.vat_check = ttk.Checkbutton(
            self.frame,
            text="VAT/OB Exemption",
            variable=self.vat_exempt,
            bootstyle=SUCCESS,
            command=self.toggle_vat_exemption,
        )
        self.vat_check.grid(
            row=12,
            column=0,
            columnspan=4,
            sticky="w",
            padx=5,
            pady=5
        )
        
        # Hourly Rate Input
        ttk.Label(
            self.frame, text="Hourly Rate (€):", font=("Arial", 12, "bold")
        ).grid(row=12, column=5, sticky="e", padx=5, pady=5)

        self.hourly_rate_var = tk.DoubleVar(value=0.0)
        self.hourly_rate_entry = ttk.Entry(
            self.frame,
            textvariable=self.hourly_rate_var,
            width=10,
            bootstyle=INFO
        )
        self.hourly_rate_entry.grid(row=12, column=6, padx=5, pady=5)        

        # ----- Items Section -----


        # Table Headers
        column_widths = [12, 40, 10, 12, 10, 12, 10]
        headers = [
            "Serial Number",
            "Description",
            "Hours",
            "Price Exc.",
            "VAT",
            "Total"
        ]
        
        ttk.Label(
            self.frame, text="Items", font=("Arial", 14, "bold"), bootstyle=PRIMARY
        ).grid(row=13, column=0, columnspan=7, pady=15)

        # Define column widths and configure grid
        self.frame.grid_columnconfigure(list(range(len(headers))), weight=1)
        
        header_frame = ttk.Frame(self.frame, bootstyle=SECONDARY)
        header_frame.grid(row=14, column=0, columnspan=len(headers), sticky="nsew")

        for idx, (header, width) in enumerate(zip(headers, column_widths)):
            ttk.Label(
                header_frame,
                text=header,
                width=width,
                bootstyle=INFO,
                anchor="center"
            ).grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

        # Items section
        self.items_frame = ttk.Frame(self.frame, bootstyle=SECONDARY)
        self.items_frame.grid(
            row=15,
            column=0,
            columnspan=len(headers),
            padx=5,
            pady=5,
            sticky="nsew"
        )

        # Configure columns for items_frame
        for idx in range(len(headers)):
            self.items_frame.grid_columnconfigure(idx, weight=1)

        self.items = []
        self.add_item_row()

        ttk.Button(
            self.frame,
            text="Add Item",
            command=self.add_item_row,
            bootstyle=(PRIMARY, OUTLINE)
        ).grid(row=16, column=0, columnspan=7, pady=10)


        # ----- Generate, Refresh, and View Invoices Buttons -----
        button_frame = ttk.Frame(self.frame, bootstyle=DARK)
        button_frame.grid(row=17, column=0, columnspan=7, pady=20)

        ttk.Button(
            button_frame,
            text="Generate Invoice",
            command=self.generate_invoice,
            bootstyle=(SUCCESS, OUTLINE),
            width=20
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_form,
            bootstyle=(WARNING, OUTLINE),
            width=20
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="View Invoices",
            command=self.view_invoices,
            bootstyle=(INFO, OUTLINE),
            width=20
        ).pack(side="left", padx=10)

        # Adjustments for aesthetics
        self.master.update()

        # Handle window close to ensure database connection is closed
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ----- Database Interaction Methods -----

    def add_invoicing_company(self):
        # Prompt user for invoicing company details
        name = simpledialog.askstring(
            "Input", "Enter Invoicing Company Name:", parent=self.master)
        if not name:
            return
        kvk = simpledialog.askstring(
            "Input", "Enter KVK Number:", parent=self.master)
        vat_nr = simpledialog.askstring(
            "Input", "Enter VAT Number:", parent=self.master)
        bank = simpledialog.askstring(
            "Input", "Enter Bank Name:", parent=self.master)
        iban = simpledialog.askstring(
            "Input", "Enter IBAN:", parent=self.master)
        bic = simpledialog.askstring(
            "Input", "Enter BIC:", parent=self.master)

        if all([name, kvk, vat_nr, bank, iban, bic]):
            success = self.db.add_invoicing_company(
                name, kvk, vat_nr, bank, iban, bic)
            if success:
                messagebox.showinfo(
                    "Success", "Invoicing Company added successfully.")
                self.invoicing_company_combo['values'] = self.db.get_invoicing_companies()
            else:
                messagebox.showerror(
                    "Error", "Invoicing Company already exists.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def add_client_company(self):
        # Prompt user for client company details
        name = simpledialog.askstring(
            "Input", "Enter Client Company Name:", parent=self.master)
        if not name:
            return
        address = simpledialog.askstring(
            "Input", "Enter Client Address:", parent=self.master)

        if all([name, address]):
            success = self.db.add_client(name, address)
            if success:
                messagebox.showinfo(
                    "Success", "Client Company added successfully.")
                self.client_company_combo['values'] = self.db.get_clients()
            else:
                messagebox.showerror(
                    "Error", "Client Company already exists.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def populate_invoicing_company_details(self, event):
        selected = self.invoicing_company_var.get()
        details = self.db.get_invoicing_company_details(selected)
        if details:
            # Populate company details
            kvk, vat_nr, bank, iban, bic = details
            self.kvk_entry.delete(0, tk.END)
            self.kvk_entry.insert(0, kvk)
            self.vat_entry.delete(0, tk.END)
            self.vat_entry.insert(0, vat_nr)
            self.bank_entry.delete(0, tk.END)
            self.bank_entry.insert(0, bank)
            self.iban_entry.delete(0, tk.END)
            self.iban_entry.insert(0, iban)
            self.bic_entry.delete(0, tk.END)
            self.bic_entry.insert(0, bic)

            # Set the next invoice number
            last_invoice_number = self.db.get_last_invoice_number(selected)
            next_invoice_number = last_invoice_number + 1
            self.invoice_number_entry.delete(0, tk.END)
            self.invoice_number_entry.insert(0, str(next_invoice_number))

    def edit_invoicing_company(self):
        company_name = self.invoicing_company_var.get()
        if not company_name:
            messagebox.showerror("Error", "Please select an invoicing company.")
            return

        details = self.db.get_invoicing_company_details(company_name)
        if not details:
            messagebox.showerror("Error", f"Details for {company_name} not found.")
            return

        kvk, vat_nr, bank, iban, bic = details

        # Create popup dialog
        dialog = tk.Toplevel(self.master)
        dialog.title(f"Edit Invoicing Company - {company_name}")

        ttk.Label(dialog, text="KVK:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        kvk_entry = ttk.Entry(dialog, width=50)
        kvk_entry.insert(0, kvk)
        kvk_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="VAT nr:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        vat_nr_entry = ttk.Entry(dialog, width=50)
        vat_nr_entry.insert(0, vat_nr)
        vat_nr_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Bank:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        bank_entry = ttk.Entry(dialog, width=50)
        bank_entry.insert(0, bank)
        bank_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="IBAN:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        iban_entry = ttk.Entry(dialog, width=50)
        iban_entry.insert(0, iban)
        iban_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="BIC:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        bic_entry = ttk.Entry(dialog, width=50)
        bic_entry.insert(0, bic)
        bic_entry.grid(row=4, column=1, padx=5, pady=5)

        def save_changes():
            new_kvk = kvk_entry.get().strip()
            new_vat_nr = vat_nr_entry.get().strip()
            new_bank = bank_entry.get().strip()
            new_iban = iban_entry.get().strip()
            new_bic = bic_entry.get().strip()

            if not all([new_kvk, new_vat_nr, new_bank, new_iban, new_bic]):
                messagebox.showerror("Error", "All fields are required.")
                return

            self.db.update_invoicing_company(company_name, new_kvk, new_vat_nr, new_bank, new_iban, new_bic)
            messagebox.showinfo("Success", f"Details for {company_name} updated successfully.")
            dialog.destroy()

        ttk.Button(dialog, text="Save Changes", command=save_changes, bootstyle=(SUCCESS, OUTLINE)).grid(
            row=5, column=0, columnspan=2, pady=10
        )



    def populate_client_company_details(self, event):
        selected = self.client_company_var.get()
        details = self.db.get_client_details(selected)
        if details:
            (address,) = details
            self.client_address_entry.delete(0, tk.END)
            self.client_address_entry.insert(0, address)
            
    def edit_client_company(self):
        client_name = self.client_company_var.get()
        if not client_name:
            messagebox.showerror("Error", "Please select a client company.")
            return

        details = self.db.get_client_details(client_name)
        if not details:
            messagebox.showerror("Error", f"Details for {client_name} not found.")
            return

        address, = details

        # Create popup dialog
        dialog = tk.Toplevel(self.master)
        dialog.title(f"Edit Client Company - {client_name}")

        ttk.Label(dialog, text="Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        address_entry = ttk.Entry(dialog, width=50)
        address_entry.insert(0, address)
        address_entry.grid(row=0, column=1, padx=5, pady=5)

        def save_changes():
            new_address = address_entry.get().strip()

            if not new_address:
                messagebox.showerror("Error", "Address field is required.")
                return

            self.db.update_client(client_name, new_address)
            messagebox.showinfo("Success", f"Details for {client_name} updated successfully.")
            dialog.destroy()

        ttk.Button(dialog, text="Save Changes", command=save_changes, bootstyle=(SUCCESS, OUTLINE)).grid(
            row=1, column=0, columnspan=2, pady=10
        )
                

    # ----- Item Management Methods -----

    # Item Row Creation

    # Function to calculate Total = Price Exc. + VAT
    def add_item_row(self):
        row = len(self.items)
        column_widths = [12, 40, 10, 12, 10, 12, 10]
        padding = {"padx": 1, "pady": 1}

        serial_label = tk.Label(
            self.items_frame,
            text=str(self.serial_number),
            width=column_widths[0],
            borderwidth=1,
            relief="solid",
            anchor="center"
        )
        description = tk.Entry(self.items_frame, width=column_widths[1])
        hours = tk.Entry(self.items_frame, width=column_widths[2])
        price_exc = tk.Entry(self.items_frame, width=column_widths[3])
        vat = tk.Entry(self.items_frame, width=column_widths[4])
        total = tk.Entry(self.items_frame, width=column_widths[5], state="readonly")
        delete_button = tk.Button(
            self.items_frame,
            text="Delete",
            command=lambda: self.delete_item_row(row),
            width=column_widths[6],
            bg="red",
            fg="white"
        )

        serial_label.grid(row=row, column=0, **padding)
        description.grid(row=row, column=1, **padding)
        hours.grid(row=row, column=2, **padding)
        price_exc.grid(row=row, column=3, **padding)
        vat.grid(row=row, column=4, **padding)
        total.grid(row=row, column=5, **padding)
        delete_button.grid(row=row, column=6, **padding)

        # Function to calculate "Price Exc." dynamically based on hours and hourly rate
        def calculate_price_exc(event=None):
            try:
                hr_rate = self.hourly_rate_var.get()  # Get the hourly rate
                hrs = float(hours.get()) if hours.get() else 0.0
                # Automatically update price_exc if it is empty or zero
                price_exc.delete(0, tk.END)
                price_exc.insert(0, f"{hr_rate * hrs:.2f}")
                calculate_total()  # Update the total
            except ValueError:
                pass  # Ignore invalid inputs

        # Function to calculate the total
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

        # Bind events to dynamically calculate values
        hours.bind("<FocusOut>", calculate_price_exc)
        price_exc.bind("<FocusOut>", calculate_total)
        vat.bind("<FocusOut>", calculate_total)

        self.items.append(
            {
                "serial": serial_label,
                "description": description,
                "hours": hours,
                "price_exc": price_exc,
                "vat": vat,
                "total": total,
                "delete_button": delete_button
            }
        )
        self.serial_number += 1


    def delete_item_row(self, row):
        if not self.items:
            return
        # Remove widgets
        item = self.items.pop(row)
        item["serial"].destroy()
        item["description"].destroy()
        item["hours"].destroy()
        item["price_exc"].destroy()
        item["vat"].destroy()
        item["total"].destroy()
        item["delete_button"].destroy()

        # Update serial numbers and row indices
        for idx, itm in enumerate(self.items):
            itm["serial"].config(text=str(idx + 1))
            itm["delete_button"].config(
                command=lambda idx=idx: self.delete_item_row(idx)
            )

        # Reset serial number counter
        self.serial_number = len(self.items) + 1

    # ----- VAT Exemption Toggle -----

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

    # ----- Invoice Generation -----

    def generate_invoice(self):
        try:
            # Collect data
            invoicing_company = self.invoicing_company_var.get().strip()
            if not invoicing_company:
                raise ValueError("Please select an Invoicing Company.")

            # Get the last invoice number and increment
            last_invoice_number = self.db.get_last_invoice_number(invoicing_company)
            next_invoice_number = last_invoice_number + 1

            # Automatically set the invoice number
            self.invoice_number_entry.delete(0, tk.END)
            self.invoice_number_entry.insert(0, str(next_invoice_number))

            client_company = self.client_company_var.get().strip()
            if not client_company:
                raise ValueError("Please select a Client Company.")

            kvk = self.kvk_entry.get().strip()
            vat_nr = self.vat_entry.get().strip()
            bank = self.bank_entry.get().strip()
            iban = self.iban_entry.get().strip()
            bic = self.bic_entry.get().strip()

            client_address = self.client_address_entry.get().strip()

            invoice_number = self.invoice_number_entry.get().strip()
            invoice_date = self.invoice_date_entry.get().strip()
            expiry_date = self.expiry_date_entry.get().strip()
            reference = self.reference_entry.get().strip()
            vat_exempt = self.vat_exempt.get()

            # Validate required fields
            required_fields = [
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
            
                        # Create PDF using invoice.py
            pdf_filename = f"Invoice_{invoice_number}.pdf"

            create_invoice_pdf(
                pdf_filename=pdf_filename,
                invoicing_company=invoicing_company,
                kvk=kvk,
                vat_nr=vat_nr,
                bank=bank,
                iban=iban,
                bic=bic,
                client_company=client_company,
                client_address=client_address,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                expiry_date=expiry_date,
                reference=reference,
                items=items,
                total_exc=total_exc,
                total_vat=total_vat,
                grand_total=grand_total,
                vat_exempt=bool(vat_exempt)
            )
            
            # Save invoice to the database
            invoice_data = {
                'invoicing_company': invoicing_company,
                'client_company': client_company,
                'invoice_number': next_invoice_number,
                'invoice_date': invoice_date,
                'expiry_date': expiry_date,
                'reference': reference,
                'total_exc': total_exc,
                'total_vat': total_vat,
                'grand_total': grand_total,
                'vat_exempt': vat_exempt,
                'pdf_filename': pdf_filename
            }
            self.db.add_invoice(invoice_data)            

            messagebox.showinfo(
                "Success", f"{pdf_filename} has been generated and saved to database."
            )
            self.refresh_form()
            
           

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # ----- Invoice History Viewer -----
    def view_invoices(self):
        company_name = self.invoicing_company_var.get()
        if not company_name:
            messagebox.showerror("Error", "Please select an invoicing company.")
            return

        invoices = self.db.get_invoices_by_company(company_name, include_erroneous=True)
        if not invoices:
            messagebox.showinfo("Info", f"No invoices found for {company_name}.")
            return

        # Create a new window to display invoices
        invoice_window = tk.Toplevel(self.master)
        invoice_window.title(f"Invoices for {company_name}")
        invoice_window.geometry("800x600")

        # Add a treeview to display invoices
        tree = ttk.Treeview(
            invoice_window,
            columns=("Invoice ID", "Invoice Number", "Date", "Client", "Total", "PDF File", "Erroneous"),
            show="headings"
        )
        tree.heading("Invoice ID", text="Invoice ID")
        tree.heading("Invoice Number", text="Invoice Number")
        tree.heading("Date", text="Date")
        tree.heading("Client", text="Client")
        tree.heading("Total", text="Total (€)")
        tree.heading("PDF File", text="PDF File")
        tree.heading("Erroneous", text="Erroneous")

        for invoice in invoices:
            is_erroneous = "Yes" if invoice[6] else "No"
            tree.insert("", "end", values=invoice[:6] + (is_erroneous,))

        tree.pack(fill="both", expand=True)

        # Function to mark an invoice as erroneous
        def mark_as_erroneous():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an invoice to mark as erroneous.")
                return

            invoice_id = tree.item(selected_item[0], "values")[0]
            self.db.mark_invoice_as_erroneous(invoice_id)
            messagebox.showinfo("Success", "Invoice marked as erroneous.")
            invoice_window.destroy()
            self.view_invoices()  # Refresh the view

        # Function to unmark an invoice as erroneous
        def unmark_as_erroneous():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an invoice to unmark as erroneous.")
                return

            invoice_id = tree.item(selected_item[0], "values")[0]
            self.db.unmark_invoice_as_erroneous(invoice_id)
            messagebox.showinfo("Success", "Invoice unmarked as erroneous.")
            invoice_window.destroy()
            self.view_invoices()  # Refresh the view

        # Add buttons for marking and unmarking erroneous invoices
        button_frame = ttk.Frame(invoice_window)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Mark as Erroneous",
            command=mark_as_erroneous,
            bootstyle=(DANGER, OUTLINE)
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Unmark Erroneous",
            command=unmark_as_erroneous,
            bootstyle=(SUCCESS, OUTLINE)
        ).grid(row=0, column=1, padx=5)





    def refresh_form(self):
        """
        Resets the entire form to its initial state.
        Clears all input fields and removes all item rows.
        """
        if messagebox.askyesno("Confirm Refresh", "Are you sure you want to reset the form?"):
            # Clear Invoicing Company Selection
            self.invoicing_company_combo.set('')
            self.kvk_entry.delete(0, tk.END)
            self.vat_entry.delete(0, tk.END)
            self.bank_entry.delete(0, tk.END)
            self.iban_entry.delete(0, tk.END)
            self.bic_entry.delete(0, tk.END)

            # Clear Client Company Selection
            self.client_company_combo.set('')
            self.client_address_entry.delete(0, tk.END)

            # Clear Invoice Metadata
            self.invoice_number_entry.delete(0, tk.END)
            self.invoice_date_entry.delete(0, tk.END)
            self.invoice_date_entry.insert(0, datetime.today().strftime("%d-%m-%Y"))
            self.expiry_date_entry.delete(0, tk.END)
            default_expiry = datetime.today() + timedelta(days=30)
            self.expiry_date_entry.insert(0, default_expiry.strftime("%d-%m-%Y"))
            self.reference_entry.delete(0, tk.END)

            # Uncheck VAT Exemption
            self.vat_exempt.set(0)
            self.toggle_vat_exemption()

            # Remove all item rows
            for item in self.items:
                item["serial"].destroy()
                item["description"].destroy()
                item["hours"].destroy()
                item["price_exc"].destroy()
                item["vat"].destroy()
                item["total"].destroy()
                item["delete_button"].destroy()
            self.items.clear()

            # Reset Serial Number Counter
            self.serial_number = 1

            # Add a new empty item row
            self.add_item_row()

    def on_closing(self):
        # Close database connection
        self.db.close()
        self.master.destroy()
