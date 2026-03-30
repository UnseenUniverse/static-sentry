# 🔍 StaticSentry

A Python-based cybersecurity scanning tool with a modern GUI built using CustomTkinter.  
This application scans files in a selected directory to detect potentially sensitive or suspicious content using keyword matching and regex-based analysis.

---

## 🚀 Features

- 🔐 **Regex-Based Secret Detection**
  - Detects credentials such as:
    - Passwords
    - API keys
    - Tokens
    - Secrets

- ⚠️ **Keyword Detection**
  - Flags suspicious terms like:
    - `urgent`, `bank`, `click here`, `free`, `flag`

- 🧠 **Severity Classification**
  - **CRITICAL** → Credentials detected  
  - **WARNING** → Suspicious keywords  
  - **SAFE** → No issues found  
  - **ERROR** → File read issues  

- 📂 **Structured Output**
  - Results grouped by file:
    - Credentials
    - Keywords  
  - Line numbers included for precise analysis  

- 🧹 **Noise Reduction**
  - Duplicate findings removed  
  - Sorted output for readability  

- 📊 **Progress Tracking**
  - Real-time progress bar during scanning  

- 🎨 **Modern GUI**
  - Built with CustomTkinter  
  - Dark mode interface  
  - Styled scrollbar and clean layout  

- 📄 **Export Reports**
  - Save scan results to a `.txt` file  

---

## 🖼️ Preview

![App Screenshot](docs/img/example.png)

---

## 🛠️ Technologies Used

- Python 3.x  
- CustomTkinter  
- Tkinter (Text + Scrollbar styling)  
- Regex (`re` module)  
- OS file traversal (`os.walk`)  

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/UnseenUniverse/static-sentry
cd static-sentry