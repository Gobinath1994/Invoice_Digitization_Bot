import requests  # Used to send HTTP requests to the local LLM API

def extract_invoice_fields(raw_text):
    """
    Sends the raw OCR text to a local LLM (via LM Studio) for structured invoice field extraction.

    Parameters:
        raw_text (str): The plain text content extracted from an invoice using OCR.

    Returns:
        str: JSON-formatted string containing the extracted fields:
            - Vendor Name
            - Invoice Number
            - Invoice Date
            - Total Amount
            - VAT Number
    """
    
    # URL of your locally running LM Studio API (adjusted for your LAN IP)
    url = "http://192.168.0.14:1234/v1/chat/completions"
    
    # Prompt that instructs the model to extract structured fields from the raw invoice text
    prompt = f"""
You are an invoice parser. Extract the following fields as JSON:
- Vendor Name
- Invoice Number
- Invoice Date
- Total Amount
- VAT Number

Text:
\"\"\"{raw_text}\"\"\"
"""

    # API request payload according to OpenAI-compatible schema
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,     # Low temperature = more predictable and consistent output
        "max_tokens": 512       # Max token output length for the model
    }

    # Send POST request to the LM Studio server
    response = requests.post(url, json=payload)

    # Return only the content part of the LLM response (a JSON string)
    return response.json()["choices"][0]["message"]["content"]