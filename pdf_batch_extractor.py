import os
import fitz  # PyMuPDF
from tqdm import tqdm

# You can configure the number of characters per text chunk
CHUNK_SIZE = 500

def clean_text(text):
    """
    Remove blank lines, page numbers, and unwanted formatting.
    """
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and not line.isdigit():  # Skip pure page numbers
            cleaned.append(line)
    return "\n".join(cleaned)

def split_text(text, method='paragraph'):
    """
    Split text into chunks based on the selected method.
    Options: 'paragraph', 'fixed', or 'page'
    """
    if method == 'paragraph':
        return text.split('\n\n')  # Split by empty lines
    elif method == 'fixed':
        return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    else:  # Treat whole page as one chunk
        return [text]

def extract_pdf_text_chunks(pdf_path, split_method='paragraph'):
    """
    Extract and clean text from a PDF file, then split into chunks.
    """
    doc = fitz.open(pdf_path)
    all_chunks = []
    for page in doc:
        text = page.get_text()
        cleaned = clean_text(text)
        chunks = split_text(cleaned, split_method)
        all_chunks.extend(chunks)
    return all_chunks

def process_folder(input_folder, output_folder, split_method='paragraph', output_format='txt'):
    """
    Process all PDF files in the input folder and save extracted text chunks.
    """
    os.makedirs(output_folder, exist_ok=True)
    print("input_dir*****"+input_folder)
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(input_folder, pdf_file)
        base_name = os.path.splitext(pdf_file)[0]
        chunks = extract_pdf_text_chunks(pdf_path, split_method)

        for i, chunk in enumerate(chunks):
            out_file = f"{base_name}_part{i+1}.{output_format}"
            out_path = os.path.join(output_folder, out_file)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(chunk)

if __name__ == "__main__":
    # Input/output folder and settings
    input_folder = "E:\\BaiduNetdiskDownload\\"          # Folder containing input PDF files
    output_folder = "E:\\baidu\\"       # Folder to store output text files
    split_method = "paragraph"     # Options: 'paragraph', 'fixed', 'page'
    output_format = "txt"          # Output file format: 'txt' or 'md'

    process_folder(input_folder, output_folder, split_method, output_format)