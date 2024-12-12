# main.py

import tkinter as tk
from gui import InvoiceApp
import logging

# Configure logging
logging.basicConfig(
    filename='invoice_app.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def main():
    root = tk.Tk()
    app = InvoiceApp(root)
    try:
        root.mainloop()
    except Exception as e:
        logging.error("Error generating invoice", exc_info=True)
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()