import os
import re
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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StaticSentry")
        self.geometry("1280x720")

        self.selected_folder = ""

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(sidebar, text="Scanner", font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(sidebar, text="Select Folder", command=self.select_folder).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Scan", command=self.scan_files).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Export", command=self.export_report).pack(pady=10, padx=10)
        ctk.CTkButton(sidebar, text="Exit", command=self.quit).pack(pady=10, padx=10)

        self.folder_label = ctk.CTkLabel(sidebar, text="No folder selected", wraplength=180)
        self.folder_label.pack(pady=10, padx=10)

        # Main
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew")

        self.main.grid_rowconfigure(3, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Keyword input
        self.keyword_entry = ctk.CTkEntry(self.main, placeholder_text="Add keyword")
        self.keyword_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(self.main, text="Add Keyword", command=self.add_keyword).grid(row=0, column=1, padx=10)

        # Progress
        self.progress = ctk.CTkProgressBar(self.main)
        self.progress.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(self.main, text="0%")
        self.progress_label.grid(row=2, column=0, columnspan=2)

        # Output
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

        # Scrollbar styling
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#3a3a3a",
            troughcolor="#1e1e1e",
            bordercolor="#1e1e1e",
            arrowcolor="#3a3a3a",
            width=8
        )

        style.map(
            "Vertical.TScrollbar",
            background=[("active", "#2a2a2a"), ("!active", "#3a3a3a")]
        )

        style.layout(
            "Vertical.TScrollbar",
            [('Vertical.Scrollbar.trough',
              {'children': [('Vertical.Scrollbar.thumb',
                             {'expand': '1', 'sticky': 'nswe'})],
               'sticky': 'ns'})]
        )

        scrollbar = ttk.Scrollbar(self.main, command=self.output.yview, style="Vertical.TScrollbar")
        scrollbar.grid(row=3, column=1, sticky="ns", pady=10)

        self.output.configure(yscrollcommand=scrollbar.set)

        # Tags
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
            percent = int((i / total) * 100)
            self.progress_label.configure(text=f"{percent}%")
            self.update_idletasks()

            try:
                with open(path, "r", errors="ignore") as f:
                    lines = f.readlines()

                found_keywords = set()
                found_credentials = set()

                for line_num, line in enumerate(lines, start=1):
                    lower = line.lower()

                    for kw in KEYWORDS:
                        if kw in lower:
                            found_keywords.add((kw, line_num))

                    for pattern in CREDENTIAL_PATTERNS:
                        matches = re.findall(pattern, lower)
                        for m in matches:
                            found_credentials.add((self.mask_value(m), line_num))

                # Sort results
                found_keywords = sorted(found_keywords, key=lambda x: x[1])
                found_credentials = sorted(found_credentials, key=lambda x: x[1])

                if found_credentials:
                    critical += 1
                    self.output.insert("end", f"[CRITICAL] {path}\n", "critical")

                    self.output.insert("end", "  Credentials:\n", "critical")
                    for c, ln in found_credentials:
                        self.output.insert("end", f"    Line {ln}: {c}\n", "critical")

                    if found_keywords:
                        self.output.insert("end", "  Keywords:\n", "warning")
                        for k, ln in found_keywords:
                            self.output.insert("end", f"    Line {ln}: {k}\n", "warning")

                elif found_keywords:
                    warnings += 1
                    self.output.insert("end", f"[WARNING] {path}\n", "warning")

                    self.output.insert("end", "  Keywords:\n", "warning")
                    for k, ln in found_keywords:
                        self.output.insert("end", f"    Line {ln}: {k}\n", "warning")

                else:
                    safe += 1
                    self.output.insert("end", f"[SAFE] {path}\n", "safe")

            except Exception as e:
                errors += 1
                self.output.insert("end", f"[ERROR] {path} ({e})\n", "error")

        self.progress.set(1)
        self.progress_label.configure(text="Complete (100%)")

        # Summary
        self.output.insert("end", "\n--- SUMMARY ---\n", "info")
        self.output.insert("end", f"Total Files: {total}\n", "info")
        self.output.insert("end", f"Critical: {critical}\n", "critical")
        self.output.insert("end", f"Warnings: {warnings}\n", "warning")
        self.output.insert("end", f"Safe: {safe}\n", "safe")
        self.output.insert("end", f"Errors: {errors}\n", "error")

    def export_report(self):
        content = self.output.get("1.0", "end")
        if not content.strip():
            messagebox.showwarning("Warning", "Nothing to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w") as f:
                f.write(content)
            messagebox.showinfo("Success", "Report saved.")

# Run
if __name__ == "__main__":
    app = App()
    app.mainloop()