import streamlit as st               # Streamlit for web interface
import re                            # Regex to extract JSON block
from ocr_engine import extract_text_from_image         # OCR from image
from genai_parser import extract_invoice_fields        # LLM extraction
from db_handler import init_db, insert_invoice, export_to_csv  # DB functions
from pdf_utils import convert_pdf_to_images            # PDF → image conversion
from validation import validate_json_fields            # Confidence scoring

def extract_json_block(text):
    """
    Extracts the first valid JSON block from a larger string.
    Useful when LLM responses contain surrounding text or formatting.

    Parameters:
        text (str): Raw LLM output

    Returns:
        str: Extracted JSON string or '{}' fallback
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"


# 🎨 Streamlit App Title
st.title("📄 Offline Invoice Digitization Bot")

# 📤 File upload (supports multiple files)
uploaded_files = st.file_uploader(
    "Upload invoices (PDF or image)", 
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# 🚀 Process uploaded files
if uploaded_files:
    st.info("Processing...")
    init_db()  # Ensure DB and table are initialized

    for uploaded_file in uploaded_files:
        st.subheader(f"📄 {uploaded_file.name}")

        # Save uploaded file to a temporary location
        ext = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp.{ext}"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Convert PDF to images or process image directly
        if ext == "pdf":
            image_paths = convert_pdf_to_images(temp_path)
        else:
            image_paths = [temp_path]

        # Process each image (PDF page or standalone)
        for img_path in image_paths:
            # 1. OCR step
            raw_text = extract_text_from_image(img_path)
            st.subheader("📝 OCR Text")
            st.text(raw_text)

            # 2. Pass OCR text to LLM
            raw_response = extract_invoice_fields(raw_text)

            # 3. Extract only the JSON portion from LLM output
            cleaned_json = extract_json_block(raw_response)

            st.subheader("📦 Extracted Fields (JSON)")
            st.code(cleaned_json, language="json")

            # 4. Validate each field and add confidence scores
            validated_data = validate_json_fields(cleaned_json)

            st.subheader("🔍 Validated Output")
            st.json(validated_data)

            # 5. Insert into MySQL database
            insert_invoice(validated_data)
            st.success("Inserted into database ✅")

# 📤 CSV Export Button
if st.button("📤 Export All to CSV"):
    export_to_csv()
    st.success("Exported to output/invoices.csv")