# Invoice Generator

A Python-based GUI application for creating and managing invoices, built using `tkinter`, `ReportLab`, and `SQLite3`. This project is designed to streamline the process of generating professional invoices, maintaining a database of invoicing companies, clients, and invoices.

---

## Features

### Invoice Management
- Add, edit, and manage invoicing companies and client details.
- Generate detailed invoices in PDF format.
- Maintain a history of invoices with options to mark invoices as erroneous.

### User-Friendly Interface
- Modern GUI designed using `ttkbootstrap` for enhanced aesthetics.
- Scrollable sections to manage long forms and itemized invoices.
- Automatic calculation of totals, including VAT.

### Database Integration
- Use `SQLite3` to store and retrieve invoicing company and client information.
- Maintain a history of generated invoices.

### Additional Features
- Dynamically calculated prices and totals.
- VAT exemption toggle.
- Error handling and logging.

---

## Requirements

### Dependencies
- Python 3.10 or higher
- `tkinter`
- `ttkbootstrap`
- `ReportLab`
- `SQLite3`

Install dependencies using the following command:
```bash
pip install ttkbootstrap reportlab
```

---

## Project Structure

```plaintext
.
├── main.py            # Entry point for the application
├── gui.py             # GUI implementation using tkinter and ttkbootstrap
├── invoice.py         # Invoice generation logic using ReportLab
├── database.py        # SQLite3 database integration
├── utils.py           # Utility functions
├── invoice_app.db     # SQLite3 database (auto-generated on first run)
├── invoice_app.log    # Log file for error tracking
└── README.md          # Project documentation
```

---

## Usage

1. Clone the repository:
```bash
git clone https://github.com/your-username/invoice-generator.git
cd invoice-generator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

---

## How to Use

### Adding an Invoicing Company
1. Click on "Add Invoicing Company".
2. Enter the company's details (e.g., KVK number, VAT number, etc.) in the prompted dialog.
3. Save the details to populate the dropdown menu.

### Adding a Client
1. Click on "Add Client Company".
2. Enter the client's name and address in the prompted dialog.
3. Save the details to populate the dropdown menu.

### Generating an Invoice
1. Select an invoicing company and client.
2. Fill in the invoice metadata (e.g., invoice number, date, reference).
3. Add items to the invoice with descriptions, hours, and prices.
4. Click on "Generate Invoice" to create a PDF and save the details to the database.

### Viewing Invoice History
1. Click on "View Invoices".
2. Browse the list of invoices for the selected company.
3. Mark invoices as erroneous or unmark them as needed.

---

## Customization

### Adding Additional Fields
To add more fields to the invoice:
1. Update the `gui.py` file to include the new field in the GUI.
2. Update the `invoice.py` file to include the field in the PDF generation.
3. Modify the database schema in `database.py` to store the additional data.

### Themes
You can customize the GUI theme by changing the `ttkbootstrap` style in `gui.py`:
```python
self.style = ttk.Style("cosmo")  # Replace "cosmo" with a preferred style
```

---

## Future Improvements
- Multi-language support for invoices.
- Exporting invoices as CSV or Excel files.
- Integration with payment gateways.
- Role-based access for multiple users.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature-name"`
4. Push to your branch: `git push origin feature-name`
5. Create a pull request.

---

## License
This project is licensed under the GNU GPL License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) for the modern tkinter themes.
- [ReportLab](https://www.reportlab.com/) for PDF generation.

---

## Author
- Darsh Modi


Feel free to reach out for feedback or questions!

