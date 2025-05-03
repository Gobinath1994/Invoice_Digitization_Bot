
# 🧾 Offline Invoice Digitization and Entry Bot (GenAI + OCR)

A complete, **offline AI-powered pipeline** to extract structured data from invoices (PDFs or images), validate it, and store it in a MySQL database. Uses **Tesseract OCR** for text extraction and a **local LLM** (like Mistral-7B via LM Studio) for intelligent field parsing.

---

## 🚀 Key Features

- 🧠 **Local GenAI Extraction (Mistral-7B)** — Extracts vendor, invoice number, date, total, and VAT from noisy OCR text
- 🔤 **OCR via Tesseract** — Converts scanned documents to raw text
- 📄 **PDF Support** — Converts PDFs to images automatically
- 📊 **Streamlit UI** — Upload files, view results, and export data interactively
- 💾 **MySQL Storage** — Stores structured data securely
- 📤 **CSV Export** — Export all records to `output/invoices.csv`
- ✅ **Offline Ready** — No cloud APIs required

---

## 📁 Project Structure

```
invoice_bot/
├── main.py                # Batch processing script (CLI)
├── webui.py               # Streamlit app for manual uploads
├── ocr_engine.py          # OCR text extractor using Tesseract
├── genai_parser.py        # Sends prompts to local LLM via LM Studio
├── db_handler.py          # MySQL logic for insert/export
├── pdf_utils.py           # Converts PDFs to images
├── validation.py          # Adds confidence scores
├── data/                  # Input files (PDFs or images)
├── output/                # Processed images, CSVs
```

---

## 🧠 How GenAI is Used

> Instead of hardcoded regex or templates, a local LLM (Mistral-7B via LM Studio) is used to **extract structured invoice fields** from raw OCR text.

### Input Example:
```
Acme Corp
Invoice No: INV-12345
Date: 04/01/2024
Total: $876.50
VAT: GB99887766
```

### Output (from LLM):
```json
{
  "Vendor Name": "Acme Corp",
  "Invoice Number": "INV-12345",
  "Invoice Date": "04/01/2024",
  "Total Amount": "$876.50",
  "VAT Number": "GB99887766"
}
```

---

## 🖥️ Requirements

- Python 3.9+
- MySQL Server (running locally)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://poppler.freedesktop.org/) (for PDF support)
- [LM Studio](https://lmstudio.ai) with a local model like `Mistral-7B`
- pip install requirements from `requirements.txt`

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd invoice_bot
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # or ./venv/Scripts/activate on Windows
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
pip install mysql-connector-python
```

### 4. Install System Tools
```bash
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt install tesseract-ocr poppler-utils
```

---

## ⚙️ LM Studio Setup

1. Install [LM Studio](https://lmstudio.ai)
2. Download a model like `mistral-7b-instruct` or `openhermes`
3. Enable **Local API Server** from Settings
4. Make sure it runs at `http://192.168.0.14:1234`

---

## 🐬 MySQL Setup

Update `db_handler.py` with your credentials:

```python
user = 'root'
password = 'Gopinath'
host = '127.0.0.1'
database = 'invoice_db'
```

The database and table will be auto-created on first run.

---

## ▶️ Running the Project

### A. CLI Batch Mode
```bash
python main.py
```
✅ Processes all files in the `/data` folder automatically

---

### B. Streamlit UI
```bash
streamlit run webui.py
```
- Upload one or more invoice files
- View OCR, extracted fields, confidence
- Insert to MySQL
- Export all to CSV

---

## 📤 Export to CSV

Click the **Export to CSV** button in the Streamlit app  
→ File will be saved to `output/invoices.csv`

---

## 🔁 How All Components Connect

```
PDF/Image
  ↓
[OCR] ocr_engine.py
  ↓
[LLM] genai_parser.py → LM Studio (Mistral-7B)
  ↓
[Scoring] validation.py
  ↓
[Storage] db_handler.py → MySQL
  ↓
[Export] export_to_csv()
```

---

## 🔄 Integration Ready

- `hubspot_sync.py` — sync invoices to HubSpot CRM
- `inspire_export.py` — export CSVs for DMS like Inspire

---

## 📌 Future Enhancements

- [ ] Line item detection
- [ ] Email integration (IMAP/Gmail)
- [ ] Docker container
- [ ] Admin dashboard

---

## 📄 License

MIT License — Free to use and modify.

---

## 🙋‍♂️ Author

**Gobinath S.**  
Built with Python, Streamlit, OCR, and local GenAI.
