# database.py

import sqlite3

class Database:
    def __init__(self, db_name="invoice_app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Table for Invoicing Companies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoicing_companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                kvk TEXT,
                vat_nr TEXT,
                bank TEXT,
                iban TEXT,
                bic TEXT
            )
        ''')
        # Table for Clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                address TEXT
            )
        ''')
        # Table for invoice history
        # Table for invoice history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoicing_company TEXT,
                client_company TEXT,
                invoice_number INTEGER,
                invoice_date TEXT,
                expiry_date TEXT,
                reference TEXT,
                total_exc REAL,
                total_vat REAL,
                grand_total REAL,
                vat_exempt INTEGER,
                pdf_filename TEXT
            )
        ''')
        # Add the is_erroneous column if it doesn't exist
        try:
            cursor.execute('ALTER TABLE invoices ADD COLUMN is_erroneous INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            # Column already exists
            pass

        self.conn.commit()

    def add_invoicing_company(self, name, kvk, vat_nr, bank, iban, bic):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO invoicing_companies (name, kvk, vat_nr, bank, iban, bic)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, kvk, vat_nr, bank, iban, bic))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Company already exists

    def get_invoicing_companies(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM invoicing_companies')
        return [row[0] for row in cursor.fetchall()]

    def get_invoicing_company_details(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT kvk, vat_nr, bank, iban, bic FROM invoicing_companies
            WHERE name = ?
        ''', (name,))
        return cursor.fetchone()

    def add_client(self, name, address):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (name, address)
                VALUES (?, ?)
            ''', (name, address))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Client already exists

    def get_clients(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM clients')
        return [row[0] for row in cursor.fetchall()]

    def get_client_details(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT address FROM clients
            WHERE name = ?
        ''', (name,))
        return cursor.fetchone()
        
    def add_invoice(self, invoice_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO invoices (
                invoicing_company, client_company, invoice_number, invoice_date,
                expiry_date, reference, total_exc, total_vat, grand_total,
                vat_exempt, pdf_filename
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            invoice_data['invoicing_company'],
            invoice_data['client_company'],
            invoice_data['invoice_number'],
            invoice_data['invoice_date'],
            invoice_data['expiry_date'],
            invoice_data['reference'],
            invoice_data['total_exc'],
            invoice_data['total_vat'],
            invoice_data['grand_total'],
            int(invoice_data['vat_exempt']),
            invoice_data['pdf_filename']
        ))
        self.conn.commit()

    def get_invoices_by_company(self, company_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT invoice_number, invoice_date, client_company, grand_total, pdf_filename
            FROM invoices WHERE invoicing_company = ?
        ''', (company_name,))
        return cursor.fetchall()
        
    def get_last_invoice_number(self, company_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT invoice_number FROM invoices
            WHERE invoicing_company = ?
            ORDER BY invoice_number DESC
            LIMIT 1
        ''', (company_name,))
        result = cursor.fetchone()
        return result[0] if result else 0  # Return 0 if no invoices exist
        
    def update_invoicing_company(self, name, kvk, vat_nr, bank, iban, bic):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE invoicing_companies
            SET kvk = ?, vat_nr = ?, bank = ?, iban = ?, bic = ?
            WHERE name = ?
        ''', (kvk, vat_nr, bank, iban, bic, name))
        self.conn.commit()

    def update_client(self, name, address):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE clients
            SET address = ?
            WHERE name = ?
        ''', (address, name))
        self.conn.commit()
    def mark_invoice_as_erroneous(self, invoice_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE invoices
            SET is_erroneous = 1
            WHERE id = ?
        ''', (invoice_id,))
        self.conn.commit()
    def get_invoices_by_company(self, company_name, include_erroneous=False):
        cursor = self.conn.cursor()
        query = '''
            SELECT id, invoice_number, invoice_date, client_company, grand_total, pdf_filename, is_erroneous
            FROM invoices
            WHERE invoicing_company = ?
        '''
        if not include_erroneous:
            query += ' AND is_erroneous = 0'

        cursor.execute(query, (company_name,))
        return cursor.fetchall()
    
    def unmark_invoice_as_erroneous(self, invoice_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE invoices
            SET is_erroneous = 0
            WHERE id = ?
        ''', (invoice_id,))
        self.conn.commit()


    

    def close(self):
        self.conn.close()
