from pdf2image import convert_from_path  # Converts PDF pages into images
import os                                # Used for file path management

def convert_pdf_to_images(pdf_path, output_folder="output"):
    """
    Converts each page of a PDF invoice into separate image files (PNG format).

    Parameters:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Directory where the generated image files will be saved.

    Returns:
        list: A list of image file paths generated from the PDF pages.
    """

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert all PDF pages to image objects using Poppler via pdf2image
    images = convert_from_path(pdf_path)

    # List to store the paths of the saved image files
    image_paths = []

    # Save each PDF page as a PNG file
    for i, page in enumerate(images):
        # Build a unique filename for each page
        path = os.path.join(
            output_folder,
            f"{os.path.basename(pdf_path)}_page{i+1}.png"
        )

        # Save the image to the output folder
        page.save(path, "PNG")

        # Add image path to the result list
        image_paths.append(path)

    # Return the list of generated image paths
    return image_paths