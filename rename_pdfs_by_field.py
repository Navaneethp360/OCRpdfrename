import os
import re
import sys
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def find_field_value(text, field_name):
    """
    Find the value of the given field_name in the text.
    Assumes the field is in the format 'Field Name: value' or 'Field Name value'.
    """
    # Create a regex pattern to find the field value
    # This pattern looks for the field name followed by optional colon and spaces, then captures the value until a line break or next field
    pattern = re.compile(rf"{re.escape(field_name)}\s*[:\-]?\s*(.+)", re.IGNORECASE)
    matches = pattern.findall(text)
    if matches:
        # Return the first match, stripped of trailing spaces and newlines
        return matches[0].strip().split('\n')[0].strip()
    return None

def rename_pdfs_by_field(folder_path, field_name):
    """Rename PDF files in the folder based on the extracted field value."""
    if not os.path.isdir(folder_path):
        print(f"Error: The folder path '{folder_path}' is not a valid directory.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            text = extract_text_from_pdf(full_path)
            if text:
                field_value = find_field_value(text, field_name)
                if field_value:
                    # Sanitize the field_value to be a valid filename
                    sanitized_value = re.sub(r'[\\/*?:"<>|]', "_", field_value)
                    new_filename = f"{sanitized_value}.pdf"
                    new_full_path = os.path.join(folder_path, new_filename)
                    # Check if new filename already exists to avoid overwriting
                    if os.path.exists(new_full_path):
                        # Append a counter suffix to make filename unique
                        base, ext = os.path.splitext(new_filename)
                        counter = 1
                        while os.path.exists(os.path.join(folder_path, f"{base}_{counter}{ext}")):
                            counter += 1
                        new_filename = f"{base}_{counter}{ext}"
                        new_full_path = os.path.join(folder_path, new_filename)
                    os.rename(full_path, new_full_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Field '{field_name}' not found in {filename}. Skipping.")
            else:
                print(f"Failed to extract text from {filename}. Skipping.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_pdfs_by_field.py <field_name>")
        print("Example: python rename_pdfs_by_field.py 'From UserID'")
        sys.exit(1)

    folder_path = os.path.dirname(os.path.abspath(__file__))
    field_name = sys.argv[1]
    rename_pdfs_by_field(folder_path, field_name)
