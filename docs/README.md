<p align="center">
  <img src="img/StaticSentry-Logo.png" width="35%" height="35%" alt="StaticSentry Logo" />
</p>
<h1 align="center"><ins>StaticSentry</ins></h1>

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-1f6feb)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Made With Love](https://img.shields.io/badge/Made%20with-Python%20%26%20Security-blueviolet)
![Cybersecurity](https://img.shields.io/badge/Focus-Cybersecurity-red)

<p align="center"> A Python-based cybersecurity scanning tool with a modern GUI built using CustomTkinter.
<p align="center"> StaticSentry scans files in a selected directory to detect potentially sensitive or suspicious content using keyword matching. Supports both pattern-based and entropy-based secret detection. </p>

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🔍 Why StaticSentry?

Hardcoded credentials and sensitive data in source code are a common security risk. StaticSentry helps identify these issues early by scanning files for patterns associated with secrets, reducing the risk of accidental exposure.

#### 💡 Use Cases

- Prevent accidental credential leaks before pushing to GitHub  
- Scan student or personal projects for sensitive data  
- Lightweight security checks for small codebases

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🚀 Features

🔐 **Regex-Based Secret Detection**

⚠️ _Note: Regex-based detection may produce false positives. StaticSentry now includes optional entropy-based analysis to improve detection of unknown or obfuscated secrets._

**Detects credentials such as:**
- Passwords
- API keys
- Tokens
- Secrets

🧬 **Entropy-Based Secret Detection (Optional)**
- Detects high-entropy strings (potential secrets) that do not match known patterns  
- Helps identify:
  - Random tokens  
  - Obfuscated credentials  
  - Unknown API keys  
- Can be enabled/disabled via the GUI  

🗝️ **Keyword Detection**
- Flags suspicious terms like:
  - `urgent`, `bank`, `click here`, `free`, `flag`

🧠 **Severity Classification**
- **CRITICAL** → Credentials detected  
- **WARNING** → Suspicious keywords  
- **SAFE** → No issues found  
- **ERROR** → File read issues  

📂 **Structured Output**
- Results grouped by file:
  - Credentials
  - Keywords  
  - Entropy matches  
- Line numbers included for precise analysis  

🧹 **Noise Reduction**
- Duplicate findings removed  
- Sorted output for readability  

📊 **Progress Tracking**
- Real-time progress bar during scanning  

🎨 **Modern GUI**
- Built with CustomTkinter  
- Dark mode interface  
- Styled scrollbar and clean layout  

📄 **Export Reports**
- `.txt` → Human-readable output
- `.json` → Structured data for integrations
- `.csv` → Spreadsheet-friendly analysis

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 📄 Example Output
Supports multiple output formats for both human readability and automation

#### TXT (Human-readable)

```bash
[CRITICAL] example.py
Credentials:
Line 3: password = "hunter2"
Line 4: api_key = "TEST-KEY-123"

Entropy Matches:
Line 10: a8f3klm9qwz...

[WARNING] config.txt
Line 10: urgent
Line 12: click here

[SAFE] clean_file.py
```

#### JSON (Structured)
```json
{
  "scan_date": "2026-04-07",
  "scanned_folder": "/project",
  "summary": {
    "critical": 1,
    "warning": 1,
    "safe": 1
  },
  "results": [
    {
      "file_name": "example.py",
      "severity": "CRITICAL",
      "credentials": [
        { "match": "password = \"hunter2\"", "line_number": 3 },
        { "match": "api_key = \"TEST-KEY-123\"", "line_number": 4 }
      ],
      "keywords": [
        { "match": "flag", "line_number": 2 }
      ],
      "entropy": [
        { "match": "a8f3klm9qwz...", "line_number": 12 }
      ]
    }
  ]
}
```

#### CSV (Spreadsheet-friendly)
_Flattened output for easy analysis in tools like Excel or Google Sheets_
```csv
file,severity,line,type,value
example.py,CRITICAL,3,credential,password = "hunter2"
example.py,CRITICAL,4,credential,api_key = "TEST-KEY-123"
example.py,CRITICAL,12,entropy,a8f3klm9qwz...
config.txt,WARNING,10,keyword,urgent
config.txt,WARNING,12,keyword,click here
```

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🖼️ Preview

![App Screenshot](img/example.png)

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🧪 Example Test File

An example file with mock credentials is included in:
`tests/sample_secrets.py`

Use it to test detection features.

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🛠️ Technologies Used

- Python 3.x  
- CustomTkinter  
- Tkinter (Text + Scrollbar styling)  
- Regex (`re` module)  
- OS file traversal (`os.walk`)  

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 📦 Requirements

- Python 3.10+
- customtkinter

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/UnseenUniverse/static-sentry
cd static-sentry
```
2. (Recommended) Create a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
3. Install dependencies:

Dependencies are listed in `requirements.txt`

4. Run the application:
```bash
python main.py
```

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 🚧 Roadmap

- Support for additional file types (JSON, YAML)
- Multithreaded scanning for performance
- Custom rule configuration via GUI

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 📜 License

This project is licensed under the MIT License.

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 👤 Maintainer

Tony Condon  
GitHub: https://github.com/UnseenUniverse  
Website: https://tonycondon.com/

<hr style="border: none; border-top: 1px solid #3b4252; margin: 2em 0;">

### 👥 Contributors

Thanks to everyone who has contributed to StaticSentry:

- [@vibeyclaw](https://github.com/vibeyclaw) – JSON/CSV export (#6)
