import os
import re
import csv
import json
import datetime
import math
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# --- Appearance ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Keywords ---
KEYWORDS = ["urgent", "password", "bank", "click here", "free", "flag"]

# --- File Types ---
ALLOWED_EXTENSIONS = (".txt", ".log", ".csv", ".py")

# --- Credential Patterns ---
CREDENTIAL_PATTERNS = [
    r'password\s*=\s*["\'].*?["\']',
    r'api[_-]?key\s*=\s*["\'].*?["\']',
    r'secret\s*=\s*["\'].*?["\']',
    r'token\s*=\s*["\'].*?["\']'
]

# --- Entropy Functions ---
def shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    length = len(data)
    for x in set(data):
        p_x = data.count(x) / length
        entropy -= p_x * math.log2(p_x)
    return entropy

def is_high_entropy_string(s, threshold=4.5, min_length=20):
    if len(s) < min_length:
        return False
    return shannon_entropy(s) >= threshold


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StaticSentry")
        self.geometry("1280x720")

        self.selected_folder = ""
        self.scan_results = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(sidebar, text="Scanner", font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(sidebar, text="Select Folder", command=self.select_folder).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Scan", command=self.scan_files).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Export", command=self.export_report).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Exit", command=self.quit).pack(pady=10, padx=10)

        self.folder_label = ctk.CTkLabel(sidebar, text="No folder selected", wraplength=180)
        self.folder_label.pack(pady=10, padx=10)

        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew")

        self.main.grid_rowconfigure(3, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self.keyword_entry = ctk.CTkEntry(self.main, placeholder_text="Add keyword")
        self.keyword_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(self.main, text="Add Keyword", command=self.add_keyword).grid(row=0, column=1, padx=10)

        self.entropy_var = tk.BooleanVar(value=True)

        self.entropy_checkbox = ctk.CTkCheckBox(
            self.main,
            text="Enable Entropy Detection",
            variable=self.entropy_var
        )
        self.entropy_checkbox.grid(row=0, column=2, padx=10)
        self.entropy_checkbox.grid(row=0, column=2, padx=10)

        self.progress = ctk.CTkProgressBar(self.main)
        self.progress.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(self.main, text="0%")
        self.progress_label.grid(row=2, column=0, columnspan=2)

        self.output = tk.Text(
            self.main,
            wrap="word",
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="flat",
            borderwidth=0
        )
        self.output.grid(row=3, column=0, padx=(10, 5), pady=10, sticky="nsew")

        style = ttk.Style()
        style.theme_use("default")

        scrollbar = ttk.Scrollbar(self.main, command=self.output.yview)
        scrollbar.grid(row=3, column=1, sticky="ns", pady=10)
        self.output.configure(yscrollcommand=scrollbar.set)

        self.output.tag_config("info", foreground="lightblue")
        self.output.tag_config("safe", foreground="lightgreen")
        self.output.tag_config("warning", foreground="orange")
        self.output.tag_config("critical", foreground="red", font=("Arial", 10, "bold"))
        self.output.tag_config("error", foreground="red")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=folder)

    def add_keyword(self):
        kw = self.keyword_entry.get().lower().strip()
        if kw:
            KEYWORDS.append(kw)
            self.output.insert("end", f"[INFO] Added keyword: {kw}\n", "info")
            self.keyword_entry.delete(0, "end")

    def mask_value(self, match):
        return re.sub(r'=["\'].*?["\']', '="****"', match)

    def scan_files(self):
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Select a folder first.")
            return

        self.output.delete("1.0", "end")
        self.scan_results = []

        critical = warnings = safe = errors = 0

        file_list = []
        for root_dir, dirs, files in os.walk(self.selected_folder):
            dirs[:] = [d for d in dirs if d not in (".venv", "__pycache__")]
            for file in files:
                if file.lower().endswith(ALLOWED_EXTENSIONS):
                    file_list.append(os.path.join(root_dir, file))

        total = len(file_list)
        if total == 0:
            messagebox.showinfo("Info", "No valid files found.")
            return

        for i, path in enumerate(file_list, start=1):
            self.output.insert("end", f"[INFO] Scanning: {path}\n", "info")

            self.progress.set(i / total)
            self.progress_label.configure(text=f"{int((i / total) * 100)}%")
            self.update_idletasks()

            try:
                with open(path, "r", errors="ignore") as f:
                    lines = f.readlines()

                found_keywords = set()
                found_credentials = set()
                found_entropy = set()

                for line_num, line in enumerate(lines, start=1):
                    lower = line.lower()

                    for kw in KEYWORDS:
                        if kw in lower:
                            found_keywords.add((kw, line_num))

                    for pattern in CREDENTIAL_PATTERNS:
                        matches = re.findall(pattern, lower)
                        for m in matches:
                            found_credentials.add((self.mask_value(m), line_num))

                    if self.entropy_var.get():
                        candidates = re.findall(r'["\'](.*?)["\']', line)
                        tokens = re.findall(r'\b\S{20,}\b', line)  # fallback for unquoted strings
                        for c in candidates + tokens:
                            if is_high_entropy_string(c):
                                found_entropy.add((c[:10] + "...", line_num))

                found_keywords = sorted(found_keywords, key=lambda x: x[1])
                found_credentials = sorted(found_credentials, key=lambda x: x[1])
                found_entropy = sorted(found_entropy, key=lambda x: x[1])

                if found_credentials or found_entropy:
                    if found_credentials:
                        severity = "CRITICAL"
                    elif found_entropy:
                        severity = "WARNING"  # softer classification
                    elif found_keywords:
                        severity = "WARNING"
                    else:
                        severity = "SAFE"
                    self.output.insert("end", f"[CRITICAL] {path}\n", "critical")

                    if found_credentials:
                        self.output.insert("end", "Credentials:\n", "critical")
                        for c, ln in found_credentials:
                            self.output.insert("end", f"Line {ln}: {c}\n", "critical")

                    if found_entropy:
                        self.output.insert("end", "Entropy Matches:\n", "critical")
                        for v, ln in found_entropy:
                            self.output.insert("end", f"Line {ln}: {v}\n", "critical")

                    if found_keywords:
                        self.output.insert("end", "Keywords:\n", "warning")
                        for k, ln in found_keywords:
                            self.output.insert("end", f"Line {ln}: {k}\n", "warning")

                elif found_keywords:
                    severity = "WARNING"
                    self.output.insert("end", f"[WARNING] {path}\n", "warning")

                    for k, ln in found_keywords:
                        self.output.insert("end", f"Line {ln}: {k}\n", "warning")

                else:
                    severity = "SAFE"
                    self.output.insert("end", f"[SAFE] {path}\n", "safe")

                self.output.insert("end", "\n")  # spacing between files

                self.scan_results.append({
                    "file_name": os.path.basename(path),
                    "file_path": path,
                    "severity": severity,
                    "credentials": [{"match": c, "line_number": ln} for c, ln in found_credentials],
                    "keywords": [{"match": k, "line_number": ln} for k, ln in found_keywords],
                    "entropy": [{"match": v, "line_number": ln} for v, ln in found_entropy],
                })

            except Exception as e:
                self.output.insert("end", f"[ERROR] {path} ({e})\n", "error")

        self.progress.set(1)
        self.progress_label.configure(text="Complete (100%)")

    def export_report(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()

        if ext == ".json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.scan_results, f, indent=2)

        elif ext == ".csv":
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["file", "severity", "line", "type", "value"])

                for r in self.scan_results:
                    for c in r["credentials"]:
                        writer.writerow([r["file_name"], r["severity"], c["line_number"], "credential", c["match"]])
                    for k in r["keywords"]:
                        writer.writerow([r["file_name"], r["severity"], k["line_number"], "keyword", k["match"]])
                    for e in r["entropy"]:
                        writer.writerow([r["file_name"], r["severity"], e["line_number"], "entropy", e["match"]])

        elif ext == ".txt":
            with open(path, "w", encoding="utf-8") as f:
                for r in self.scan_results:
                    f.write(f"[{r['severity']}] {r['file_name']}\n")

                    for c in r["credentials"]:
                        f.write(f"Line {c['line_number']}: {c['match']} (credential)\n")

                    for k in r["keywords"]:
                        f.write(f"Line {k['line_number']}: {k['match']} (keyword)\n")

                    for e in r["entropy"]:
                        f.write(f"Line {e['line_number']}: {e['match']} (entropy)\n")

                    f.write("\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()