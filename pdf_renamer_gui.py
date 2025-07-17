import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import fitz  # PyMuPDF
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# File Rename App
class GlassPDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Renamer")
        self.root.geometry("800x600")
        self.root.configure(bg="#dbe9f4")

        self.setup_ui()

    def glass_frame(self, parent, **kwargs):
        frame = tk.Frame(parent, bg="#ffffff", bd=0, highlightthickness=0, **kwargs)
        frame.config(
            bg="#ffffff",
            highlightbackground="#ffffff",
            highlightcolor="#ffffff"
        )
        frame.pack_propagate(False)
        return frame

    def setup_ui(self):
        # Field Frame
        field_frame = self.glass_frame(self.root)
        field_frame.place(x=20, y=20, width=760, height=50)

        tb.Label(field_frame, text="Field Name:", font=("Segoe UI", 10, "bold"), background="#ffffff").pack(side="left", padx=10)
        self.field_entry = tb.Entry(field_frame, bootstyle="light", width=50)
        self.field_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        # Folder Frame
        folder_frame = self.glass_frame(self.root)
        folder_frame.place(x=20, y=80, width=760, height=50)

        tb.Label(folder_frame, text="Folder:", font=("Segoe UI", 10, "bold"), background="#ffffff").pack(side="left", padx=10)
        self.folder_var = tk.StringVar()
        self.folder_entry = tb.Entry(folder_frame, textvariable=self.folder_var, bootstyle="light", width=50, state="readonly")
        self.folder_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        tb.Button(folder_frame, text="Browse", bootstyle="PRIMARY", command=self.browse_folder).pack(side="left", padx=5)

        # Buttons Frame
        button_frame = self.glass_frame(self.root)
        button_frame.place(x=20, y=140, width=760, height=50)

        tb.Button(button_frame, text="Preview PDF", bootstyle="INFO", command=self.preview_pdf).pack(side="left", expand=True, fill="x", padx=5, pady=5)
        tb.Button(button_frame, text="Rename PDFs", bootstyle="SUCCESS", command=self.start_rename).pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # Console Frame
        console_frame = self.glass_frame(self.root)
        console_frame.place(x=20, y=200, width=760, height=330)

        tk.Label(console_frame, text="Console Output:", font=("Segoe UI", 10, "bold"), background="#ffffff").pack(anchor="w", padx=10, pady=5)
        self.console = tk.Text(console_frame, bg="#ffffff", relief="flat", wrap="word", fg="#333", font=("Segoe UI", 9))
        self.console.pack(fill="both", expand=True, padx=10, pady=5)

        # Footer
        footer = tk.Label(self.root, text="Developed by Navaneeth P - 2025", bg="#dbe9f4", fg="#555", font=("Segoe UI", 9), cursor="hand2")
        footer.place(x=0, y=570, width=800)
        footer.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Navaneethp360"))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

    def extract_text_from_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            return ''.join(page.get_text() for page in doc)
        except Exception as e:
            self.log(f"Error reading {pdf_path}: {e}")
            return None

    def find_field_value(self, text, field_name):
        pattern = re.compile(rf"{re.escape(field_name)}\s*[:\-]?\s*(.+)", re.IGNORECASE)
        matches = pattern.findall(text)
        return matches[0].strip().split('\n')[0].strip() if matches else None

    def rename_pdfs_by_field(self, folder_path, field_name):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(folder_path, filename)
                self.log(f"Processing: {filename}")
                text = self.extract_text_from_pdf(full_path)
                if text:
                    value = self.find_field_value(text, field_name)
                    if value:
                        safe_name = re.sub(r'[\\/*?:"<>|]', "_", value) + ".pdf"
                        target_path = os.path.join(folder_path, safe_name)
                        counter = 1
                        while os.path.exists(target_path):
                            target_path = os.path.join(folder_path, f"{safe_name[:-4]}_{counter}.pdf")
                            counter += 1
                        os.rename(full_path, target_path)
                        self.log(f"Renamed to: {os.path.basename(target_path)}")
                    else:
                        self.log(f"Field '{field_name}' not found in {filename}")
                else:
                    self.log(f"Could not extract text from {filename}")

    def start_rename(self):
        field_name = self.field_entry.get().strip()
        folder_path = self.folder_var.get().strip()
        if not field_name or not folder_path:
            messagebox.showerror("Error", "Please provide both Field Name and Folder Path.")
            return
        self.console.delete(1.0, tk.END)
        threading.Thread(target=self.rename_pdfs_by_field, args=(folder_path, field_name), daemon=True).start()

    def preview_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return
        text = self.extract_text_from_pdf(pdf_path)
        if text is None:
            messagebox.showerror("Error", "Failed to extract text.")
            return
        preview = tk.Toplevel(self.root)
        preview.title(f"Preview - {os.path.basename(pdf_path)}")
        preview.geometry("600x400")
        text_widget = tk.Text(preview, wrap="word", bg="#f9f9f9", fg="#333", relief="flat")
        text_widget.insert(tk.END, text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = tb.Window(themename="flatly")
    GlassPDFRenamerApp(app)
    app.mainloop()
