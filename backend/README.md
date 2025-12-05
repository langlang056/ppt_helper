# UniTutor AI - Backend

FastAPI backend for the Multi-Agent Courseware Explainer.

## Phase 1 Status ✅

**Completed Features:**
- ✅ PDF upload and validation
- ✅ LlamaParse integration for parsing complex slides
- ✅ SQLite caching to avoid redundant API calls
- ✅ Basic API endpoints (`/upload`, `/explain`)
- ✅ Automatic duplicate detection via file hashing

**Next Steps (Phase 2):**
- LangGraph multi-agent workflow (Navigator → Professor → Tutor)
- Claude 3.5 Sonnet integration
- Structured explanation generation in Chinese

---

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- [LlamaCloud API Key](https://cloud.llamaindex.ai/api-key)
- [Anthropic API Key](https://console.anthropic.com/) (for Phase 2)

### 2. Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
LLAMA_CLOUD_API_KEY=llx-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 4. Run the Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

---

## API Endpoints

### 1. Upload PDF
```http
POST /api/upload
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "pdf_id": "a3f2d9c8b1e4f5a6",
  "total_pages": 42,
  "filename": "lecture_notes.pdf",
  "message": "PDF uploaded and parsed successfully"
}
```

### 2. Get Page Explanation
```http
GET /api/explain/{pdf_id}/{page_number}
```

**Response (Phase 1 - Basic):**
```json
{
  "page_number": 5,
  "page_type": "CONTENT",
  "content": {
    "summary": "第 5 页内容(待 AI 处理)",
    "key_points": [
      {
        "concept": "原始文本",
        "explanation": "Extracted text preview...",
        "is_important": false
      }
    ],
    "analogy": "[将在 Phase 2 添加 LangGraph 处理]",
    "example": ""
  },
  "original_language": "mixed"
}
```

### 3. Get PDF Info
```http
GET /api/pdf/{pdf_id}/info
```

---

## Testing

### Manual Test with cURL

```bash
# 1. Upload a test PDF
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@test_lecture.pdf"

# 2. Get explanation for page 1 (replace {pdf_id} with response from step 1)
curl "http://localhost:8000/api/explain/a3f2d9c8b1e4f5a6/1"
```

### Test with Python

```python
import requests

# Upload
with open("test.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": f}
    )
print(response.json())

# Get explanation
pdf_id = response.json()["pdf_id"]
explanation = requests.get(
    f"http://localhost:8000/api/explain/{pdf_id}/1"
)
print(explanation.json())
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & routes
│   ├── config.py            # Settings management
│   ├── agents/              # (Phase 2) LangGraph agents
│   ├── models/
│   │   ├── database.py      # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   └── services/
│       ├── pdf_parser.py    # LlamaParse integration
│       └── cache_service.py # Database caching
├── uploads/                 # Stored PDFs
├── temp/                    # Temporary files
├── requirements.txt
└── .env
```

---

## Troubleshooting

### Issue: "LLAMA_CLOUD_API_KEY not found"
**Solution:** Make sure `.env` file exists and contains valid API key.

### Issue: "Unable to parse PDF"
**Solution:**
- Check PDF is not password-protected
- Ensure file size < 50MB
- Verify LlamaParse API key is active

### Issue: Database errors
**Solution:** Delete `unitutor.db` and restart the server to recreate tables.

---

## Phase 2 Preview

Next implementation will add:

1. **Navigator Agent** - Classify page type (TITLE/CONTENT/END)
2. **Professor Agent** - Extract academic concepts in original language
3. **Tutor Agent** - Generate Chinese explanations with analogies
4. **Formatter Agent** - Structure output into final JSON

Stay tuned! 🚀
