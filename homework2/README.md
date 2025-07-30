# 🗂️ Week 2 Assignment – Corpus Construction Pipeline

## 🎯 Goal

The goal of this assignment is to build a **corpus construction pipeline** that collects raw data (text, image, or audio), extracts useful content, cleans it, removes duplicates, and exports it in structured JSON format. This corpus can later be used to fine-tune or evaluate machine learning models.

---

## 🧩 Pipeline Steps

### 1. Data Collection

- Sources used:
  - Web pages (via `requests` + `BeautifulSoup`)
  - PNG images (scanned documents)
  - MP3 audio files (Mandarin speech)
- All data was stored in `input/` folder

### 2. Content Extraction

- **Images:** Used Tesseract OCR (`pytesseract`) to extract text from `.png`
- **Audio:** Used OpenAI Whisper (`whisper`) to transcribe `.mp3` files
- **Web:** Used `BeautifulSoup` to parse and extract raw text from HTML pages

### 3. Cleaning

- Removed extra whitespace, special symbols, HTML tags
- Normalized text (lowercasing, punctuation cleanup)
- Filtered out short or irrelevant content (e.g., text under 10 characters)

### 4. Deduplication

- Applied MinHash + Jaccard similarity to detect and drop near-duplicate entries

### 5. Export

- Final structured corpus saved as `data.json`
- Each entry includes:
  ```json
  {
    "source": "input/audio/sample1.mp3",
    "text": "你好，欢迎来到自然语言处理课程。"
  }
