from PIL import Image          # Used to open and manipulate image files
import pytesseract             # Python wrapper for Tesseract OCR engine

def extract_text_from_image(image_path):
    """
    Performs OCR (Optical Character Recognition) on the given image.

    Parameters:
        image_path (str): The path to the invoice image (PNG, JPG, etc.)

    Returns:
        str: The raw text content extracted from the image using Tesseract OCR
    """
    # Open the image using Pillow (PIL)
    image = Image.open(image_path)

    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Return the OCR result as plain text
    return extracted_text