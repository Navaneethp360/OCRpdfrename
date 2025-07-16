# 🗂️ OCR PDF Rename App

A Python-based desktop tool that automatically renames PDF files by extracting specific text fields inside each document.  
Perfect for bulk renaming documents like certificates, reports, or forms based on their content.


---

## 🔧 Features

- 🖥️ **Modern GUI Interface** with custom-styled `tkinter`
- 📝 **Extract & Rename**: Automatically renames PDFs based on a specified field inside the PDF
- 🔎 **Preview Mode**: View extracted text before renaming to pick what field you need to use for renaming
- 🖂 **Batch Processing**: Process all PDFs inside a folder with one click
- 📝 **Smart Filename Handling**:  
  - Replaces invalid filename characters  
  - Automatically appends counters for duplicate names
- 🖨️ **Live Console Log**: Real-time operation logs inside the app

---

## 🛠️ Built With

| Tool         | Purpose                         |
|--------------|---------------------------------|
| `tkinter`   | GUI window and controls         |
| `PyMuPDF` (`fitz`) | PDF text extraction      |
| `threading` | Background operations           |
| `re`        | Regular expression parsing      |
| `os`        | File system operations          |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Navaneethp360/pdf-renamer-app.git
cd pdf-renamer-app
pip install pymupdf
python pdf_renamer_gui.py
```
### 2. Run the App:
You can run the application either by using python pdf_renamer_gui.py command in cmd 

OR

Locate the .exe file in the dist folder and run the application.

## 🎨 Screenshots
<img width="600" height="578" alt="image" src="https://github.com/user-attachments/assets/4011f191-0eda-4c4d-88a0-68b592e136ff" />


## 📌 Notes
Designed for Windows OS

Tested with Python 3.10+

Requires PyMuPDF for PDF text extraction

Runs as a standalone GUI app

## 🧑‍💻 Developed By
Navaneeth P — 2025

Feel free to connect or contribute!

