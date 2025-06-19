
# resume_parser.py
import os
import re
import json
import spacy
from docx import Document
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

CATEGORY_KEYWORDS = {
    "Data Science": ["machine learning", "data analysis", "python", "pandas", "numpy"],
    "Web Development": ["javascript", "react", "html", "css", "frontend", "backend"],
    "Database Administration": ["sql", "oracle", "database", "dbms", "dba"],
    "Cybersecurity": ["security", "network", "firewall", "vulnerability", "pen testing"]
}


def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format")


def parse_resume(text):
    doc = nlp(text)
    name = None
    email = None
    phone = None

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"\+?\d[\d\s\-]{8,}\d", text)

    email = email_match.group() if email_match else None
    phone = phone_match.group() if phone_match else None

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "text": text
    }


def categorize_resume(text):
    categories = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            categories.append(category)
    return categories or ["Uncategorized"]


def process_resume(file_path):
    text = extract_text_from_file(file_path)
    parsed = parse_resume(text)
    parsed["category"] = categorize_resume(text)
    return parsed


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog, messagebox

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("Resume files", "*.pdf *.docx")])
        if file_path:
            result = process_resume(file_path)
            output.delete("1.0", tk.END)
            output.insert(tk.END, json.dumps(result, indent=2))

    root = tk.Tk()
    root.title("Resume Parser and Categorizer")
    root.geometry("700x500")

    tk.Button(root, text="Select Resume", command=select_file).pack(pady=10)
    output = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
    output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    root.mainloop()
