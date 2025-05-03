import mysql.connector  # MySQL client for Python
import json             # To handle JSON structures

# === MySQL Connection Info ===
# These are your database credentials for local MySQL
user = 'root'
password = 'Gopinath'
host = '127.0.0.1'
database = 'invoice_db'  # The database name to use or create


def init_db():
    """
    Initialize the MySQL database and ensure the required table exists.
    - Creates 'invoice_db' if it doesn't exist
    - Creates 'invoices' table if it doesn't exist
    """
    # Connect to MySQL server without specifying a DB yet
    conn = mysql.connector.connect(user=user, password=password, host=host)
    cursor = conn.cursor()

    # Create the database if not already present
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    
    # Switch to the created or existing database
    conn.database = database

    # Create the invoices table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        vendor VARCHAR(255),
        invoice_number VARCHAR(255),
        date VARCHAR(255),
        total FLOAT,
        vat_number VARCHAR(255)
    )
    """)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_invoice(data):
    """
    Inserts a validated invoice record (Python dict) into the invoices table.
    Expects the input format with nested structure:
    {
        "Vendor Name": {"value": "..."},
        "Invoice Number": {"value": "..."},
        ...
    }
    """
    # Connect to the invoice_db database
    conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = conn.cursor()

    # Helper function to extract nested 'value' safely
    def safe_value(key):
        return data.get(key, {}).get("value", "")

    # SQL insert query
    sql = """
    INSERT INTO invoices (vendor, invoice_number, date, total, vat_number)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Clean and parse 'Total Amount'
    # Remove dollar sign and commas, convert to float
    total_raw = safe_value("Total Amount").replace('$', '').replace(',', '')
    total = float(total_raw) if total_raw else 0.0

    # Prepare values for insertion
    values = (
        safe_value("Vendor Name"),
        safe_value("Invoice Number"),
        safe_value("Invoice Date"),
        total,
        safe_value("VAT Number")
    )

    # Execute the SQL insert statement
    cursor.execute(sql, values)

    # Commit and close the DB connection
    conn.commit()
    conn.close()


def export_to_csv(path="output/invoices.csv"):
    """
    Exports all invoice records from the MySQL database to a CSV file.
    Default path: output/invoices.csv
    """
    import csv  # Import CSV module inside the function

    # Connect to the invoice_db database
    conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = conn.cursor()

    # Query all records from the invoices table
    cursor.execute("SELECT vendor, invoice_number, date, total, vat_number FROM invoices")
    rows = cursor.fetchall()

    # Define CSV headers
    headers = ["Vendor", "Invoice Number", "Date", "Total", "VAT Number"]

    # Write data to CSV file
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)      # Write column headers
        writer.writerows(rows)        # Write all data rows

    # Close the DB connection
    conn.close()