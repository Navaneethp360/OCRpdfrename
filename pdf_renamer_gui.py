import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import webbrowser
import fitz  # PyMuPDF

class PDFRenamerGUI:
    ACCENT_COLOR = "#007acc"
    BG_COLOR = "#ffffff"
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 10

    def __init__(self, root):
        self.root = root
        self.root.title("PDF Renamer")
        self.root.configure(bg=self.BG_COLOR)
        self.style = ttk.Style()
        self.style.theme_use('default')

        # Configure style for ttk buttons with accent color
        self.style.configure('Accent.TButton',
                             background=self.ACCENT_COLOR,
                             foreground='white',
                             font=(self.FONT_FAMILY, self.FONT_SIZE),
                             borderwidth=0,
                             focusthickness=3,
                             focuscolor='none',
                             padding=6)
        self.style.map('Accent.TButton',
                       background=[('active', '#005a9e')],
                       foreground=[('active', 'white')])

        # Configure style for ttk entry
        self.style.configure('TEntry',
                             font=(self.FONT_FAMILY, self.FONT_SIZE),
                             padding=5)

        # Configure style for labels
        label_font = (self.FONT_FAMILY, self.FONT_SIZE)

        # Field name input
        field_frame = ttk.Frame(self.root)
        field_frame.pack(padx=10, pady=5, fill='x')
        ttk.Label(field_frame, text="Field Name:", font=label_font).pack(side='left', padx=(0,5))
        self.field_entry = ttk.Entry(field_frame, width=40)
        self.field_entry.pack(side='left', fill='x', expand=True)

        # Folder selection
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(padx=10, pady=5, fill='x')
        ttk.Label(folder_frame, text="Folder:", font=label_font).pack(side='left', padx=(0,5))
        self.folder_path_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=40, state='readonly')
        self.folder_entry.pack(side='left', fill='x', expand=True)
        self.browse_button = ttk.Button(folder_frame, text="Browse...", command=self.browse_folder, style='Accent.TButton')
        self.browse_button.pack(side='left', padx=5)

        # Buttons frame
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(padx=10, pady=10, fill='x')
        self.rename_button = ttk.Button(buttons_frame, text="Rename PDFs", command=self.start_rename, style='Accent.TButton')
        self.rename_button.pack(side='left', expand=True, fill='x', padx=(0,5))
        self.preview_button = ttk.Button(buttons_frame, text="Preview PDF", command=self.preview_pdf, style='Accent.TButton')
        self.preview_button.pack(side='left', expand=True, fill='x', padx=(5,0))

        # Log console label
        ttk.Label(self.root, text="Console Output:", font=label_font).pack(anchor='w', padx=10, pady=(10,0))
        # Log console text widget
        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=20, state='disabled', font=(self.FONT_FAMILY, self.FONT_SIZE))
        self.log_text.pack(padx=10, pady=5, fill='both', expand=True)

        # Footer with clickable link
        self.footer_label = tk.Label(
            self.root,
            text="Developed by: Navaneeth P - 2025",
            bg=self.BG_COLOR,
            fg="blue",
            cursor="hand2",
            font=(self.FONT_FAMILY, self.FONT_SIZE - 2, "underline"))
        self.footer_label.pack(side=tk.BOTTOM, pady=10)
        self.footer_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Navaneethp360"))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def extract_text_from_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            self.log(f"Error reading {pdf_path}: {e}")
            return None

    def find_field_value(self, text, field_name):
        pattern = re.compile(rf"{re.escape(field_name)}\s*[:\-]?\s*(.+)", re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            return matches[0].strip().split('\n')[0].strip()
        return None

    def rename_pdfs_by_field(self, folder_path, field_name):
        if not os.path.isdir(folder_path):
            self.log(f"Error: The folder path '{folder_path}' is not a valid directory.")
            return

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(folder_path, filename)
                self.log(f"Processing file: {filename}")
                text = self.extract_text_from_pdf(full_path)
                if text:
                    field_value = self.find_field_value(text, field_name)
                    if field_value:
                        sanitized_value = re.sub(r'[\\/*?:"<>|]', "_", field_value)
                        new_filename = f"{sanitized_value}.pdf"
                        new_full_path = os.path.join(folder_path, new_filename)
                        if os.path.exists(new_full_path):
                            base, ext = os.path.splitext(new_filename)
                            counter = 1
                            while os.path.exists(os.path.join(folder_path, f"{base}_{counter}{ext}")):
                                counter += 1
                            new_filename = f"{base}_{counter}{ext}"
                            new_full_path = os.path.join(folder_path, new_filename)
                        os.rename(full_path, new_full_path)
                        self.log(f"Renamed '{filename}' to '{new_filename}'")
                    else:
                        self.log(f"Field '{field_name}' not found in {filename}. Skipping.")
                else:
                    self.log(f"Failed to extract text from {filename}. Skipping.")

    def start_rename(self):
        field_name = self.field_entry.get().strip()
        folder_path = self.folder_path_var.get().strip()
        if not field_name:
            messagebox.showerror("Input Error", "Please enter the field name.")
            return
        if not folder_path:
            messagebox.showerror("Input Error", "Please select a folder.")
            return
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        # Run renaming in a separate thread to keep GUI responsive
        threading.Thread(target=self.rename_pdfs_by_field, args=(folder_path, field_name), daemon=True).start()

    def preview_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return
        text = self.extract_text_from_pdf(pdf_path)
        if text is None:
            messagebox.showerror("Error", "Failed to extract text from the selected PDF.")
            return
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview: {os.path.basename(pdf_path)}")
        text_widget = scrolledtext.ScrolledText(preview_window, width=80, height=30)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, text)
        text_widget.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFRenamerGUI(root)
    root.mainloop()
