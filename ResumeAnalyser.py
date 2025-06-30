import os
import fitz
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def truncate_resume(text, max_chars=2000):
    return text.strip()[:max_chars]

def suggest_job_using_ai(resume_text):
    trimmed_text = truncate_resume(resume_text)

    prompt = f"""
You are an AI job analyzer. Based on the resume below, suggest:
1. A professional and suitable Job Title
2. A concise and relevant Job Description

Resume:
\"\"\"{trimmed_text}\"\"\"

Respond in this format:
Job Title: ...
Job Description: ...
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def analyze_resume():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, f"📄 Selected File: {os.path.basename(file_path)}\n\n")

    text = extract_text_from_pdf(file_path)
    if "Error" in text:
        output_box.insert(tk.END, text)
        return

    try:
        suggestion = suggest_job_using_ai(text)
        output_box.insert(tk.END, suggestion)
    except Exception as e:
        output_box.insert(tk.END, f"❌ Error: {str(e)}")

root = tk.Tk()
root.title("AI Resume Analyzer (Groq-powered)")
root.geometry("700x500")
root.resizable(False, False)

title_label = tk.Label(root, text="Upload PDF Resume to Get Job Suggestion", font=("Helvetica", 14, "bold"))
title_label.pack(pady=10)

upload_btn = tk.Button(root, text="Select Resume PDF", command=analyze_resume, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
upload_btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Courier", 10))
output_box.pack(padx=10, pady=10)

root.mainloop()
