# Invoice Generator

A Python-based GUI application for creating and managing invoices, built using `tkinter`, `ReportLab`, and `SQLite3`. This project is designed to streamline the process of generating professional invoices, maintaining a database of invoicing companies, clients, and invoices. This app is also completely local, so no worries about a server being compromised in a faraway land with a company that "apologizes" for data leaks the size of a supermassive black hole.

Of course, there may be bugs, and I would be happy to fix them if you let me know, or if you're really generous and fix them yourself :)

I hope this tool is useful, and saves you the headache of making invoices. If you are unfamiliar with Python, then I made a .exe version of the application to be used as an end user. 

# Download the `.exe` File for This Project

This repository is set up to automatically generate an `.exe` file for this project using GitHub Actions. You can download the executable directly from the repository without needing to manually run any packaging tools. Here's how:

---

## Steps to Download the `.exe` File

1. **Go to the Actions Tab**  
   - Navigate to the [Actions](../../actions) tab in this GitHub repository.

2. **Select the Latest Workflow Run**  
   - Find the most recent workflow run triggered by a push or pull request to the `main` branch.  
   - Click on the workflow name (e.g., "Build EXE").

3. **Download the Artifact**  
   - Scroll down to the **Artifacts** section in the workflow summary.  
   - You’ll find a downloadable artifact named `python-app-exe` (or a similar name).  
   - Click on it to download the `.exe` file.

4. **Run the `.exe` File**  
   - Extract the `.exe` file (if needed).  
   - Double-click the `.exe` file to run the application. No additional setup is required.

---

## Additional Notes

- The `.exe` file is built using `pyinstaller` to ensure it works as a standalone executable on Windows systems.
- If you encounter issues or need the application for a different platform, feel free to open an issue in the repository.

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
pip install -r requirements.txt
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
├── requirements.txt   # Dependencies for the project
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

## Packaging as an Executable

If you want to use the application without requiring Python installation, you can package it as an executable using `pyinstaller`:

1. Install `pyinstaller`:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
pyinstaller --onefile --noconsole main.py
```

3. The executable will be located in the `dist` folder. Share this file with users who can run the application without installing Python.

---

## Possible Future Improvements
- Multi-language support for invoices (let's be real, Dutch would probably be the only other language added).
- A better GUI (Python may not have been the right choice for this).
- Tax calculation and management for each of your companies.
- Integration with email to directly send invoices and keep track of them in your local database.
- Role-based access for multiple users.

Feel free to pick up any one you think would be the most helpful and contribute! They are not listed in any particular order of importance.
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
![app_screen](https://github.com/user-attachments/assets/76ed94fa-575f-4bf3-b846-fcc7ae15ce85)

![invoice_example](https://github.com/user-attachments/assets/ff1d8a92-d73a-4746-970c-36d4924a3a13)


## Acknowledgments
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) for the modern tkinter themes.
- [ReportLab](https://www.reportlab.com/) for PDF generation.

---

## Author
- Darsh Modi

Feel free to reach out for feedback or questions!

