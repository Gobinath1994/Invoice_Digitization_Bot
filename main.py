import os  # For file operations and directory traversal
import re  # For regex to clean JSON blocks from LLM responses

# Custom modules for each part of the pipeline
from ocr_engine import extract_text_from_image                # OCR function
from genai_parser import extract_invoice_fields               # Local LLM invoice field extraction
from db_handler import init_db, insert_invoice                # MySQL DB setup and data insertion
from pdf_utils import convert_pdf_to_images                   # Converts PDF to images
from validation import validate_json_fields                   # Applies confidence scoring and field validation

def extract_json_block(text):
    """
    Extracts the first JSON block from a string using regular expressions.
    Useful for cleaning LLM responses that contain extra text before/after the JSON.

    Parameters:
        text (str): Raw string from LLM output

    Returns:
        str: Clean JSON string, or "{}" if none found
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else "{}"

def process_invoice(image_path):
    """
    Complete processing pipeline for a single invoice image:
    - OCR text extraction
    - LLM field extraction
    - Validation and confidence scoring
    - Insert into MySQL

    Parameters:
        image_path (str): Path to image file to be processed
    """
    print(f"[INFO] Processing: {image_path}")

    # Step 1: Extract text via OCR
    raw_text = extract_text_from_image(image_path)
    print("[INFO] OCR Text Extracted.")

    # Step 2: Send text to LLM to extract fields
    raw_response = extract_invoice_fields(raw_text)
    print("[INFO] JSON Extracted from LLM:\n", raw_response)

    # Step 3: Clean up JSON if response includes extra text
    cleaned_json = extract_json_block(raw_response)

    # Step 4: Validate fields (adds confidence score)
    validated_data = validate_json_fields(cleaned_json)

    # Step 5: Insert structured data into MySQL
    insert_invoice(validated_data)
    print("[INFO] Data inserted into database.\n")

def main():
    """
    Main entry point of the script.
    Scans the 'data/' folder and processes each invoice file (PDF or image).
    """
    # Ensure the database and table are ready
    init_db()

    # Path to folder containing invoice files
    invoice_dir = "data"

    # Iterate over all files in the folder
    for file in os.listdir(invoice_dir):
        file_path = os.path.join(invoice_dir, file)

        # If file is a PDF, convert to images first
        if file.lower().endswith(".pdf"):
            images = convert_pdf_to_images(file_path)
            for img in images:
                process_invoice(img)

        # If file is an image, process directly
        elif file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
            process_invoice(file_path)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()