# 🚀 Quick Reference Card

One-page cheat sheet for UniTutor AI backend.

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Setup
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env: Add LLAMA_CLOUD_API_KEY

# 3. Run
python -m uvicorn app.main:app --reload

# 4. Test
http://localhost:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint                              | Purpose                 |
| ------ | ------------------------------------- | ----------------------- |
| GET    | `/`                                   | Health check            |
| POST   | `/api/upload`                         | Upload PDF              |
| GET    | `/api/explain/{pdf_id}/{page_number}` | Get page explanation    |
| GET    | `/api/pdf/{pdf_id}/info`              | Get PDF metadata        |

---

## 💻 Example Usage

### Python
```python
import requests

# Upload
files = {"file": open("lecture.pdf", "rb")}
r = requests.post("http://localhost:8000/api/upload", files=files)
pdf_id = r.json()["pdf_id"]

# Get explanation
r = requests.get(f"http://localhost:8000/api/explain/{pdf_id}/1")
print(r.json()["content"]["summary"])
```

### cURL
```bash
# Upload
curl -X POST "http://localhost:8000/api/upload" -F "file=@test.pdf"

# Explain
curl "http://localhost:8000/api/explain/{pdf_id}/1"
```

---

## 📂 File Structure

```
backend/
├── app/
│   ├── main.py              # Routes
│   ├── config.py            # Settings
│   ├── models/
│   │   ├── database.py      # DB models
│   │   └── schemas.py       # API schemas
│   └── services/
│       ├── pdf_parser.py    # LlamaParse
│       └── cache_service.py # Caching
├── requirements.txt         # Dependencies
├── .env                     # API keys
└── test_api.py              # Tests
```

---

## 🔧 Configuration (.env)

```env
LLAMA_CLOUD_API_KEY=llx-your-key-here
ANTHROPIC_API_KEY=sk-ant-for-phase-2
DATABASE_URL=sqlite+aiosqlite:///./unitutor.db
MAX_FILE_SIZE_MB=50
DEBUG=True
```

---

## 🗄️ Database Schema

### pdf_documents
```sql
id (PK) | filename | total_pages | file_path | uploaded_at
```

### page_explanations
```sql
id (PK) | pdf_id | page_number | explanation_json | created_at
```

---

## 🐛 Common Issues

| Error                           | Fix                       |
| ------------------------------- | ------------------------- |
| "LLAMA_CLOUD_API_KEY not found" | Check `.env` file exists  |
| "Connection refused"            | Start server first        |
| "Failed to parse PDF"           | Check PDF not encrypted   |
| Import errors                   | `pip install -r requirements.txt` |

---

## 📊 Response Format

```json
{
  "page_number": 1,
  "page_type": "CONTENT",
  "content": {
    "summary": "一句话总结",
    "key_points": [
      {
        "concept": "概念名",
        "explanation": "解释",
        "is_important": true
      }
    ],
    "analogy": "类比",
    "example": "实例"
  },
  "original_language": "fr"
}
```

---

## 💰 Costs

| Service    | Per Page | Monthly (250 pages/day) |
| ---------- | -------- | ----------------------- |
| LlamaParse | $0.003   | $22.50                  |
| Claude*    | $0.02    | $150 → $30 (with cache) |

*Phase 2 only

---

## 🧪 Testing

```bash
# Interactive docs
http://localhost:8000/docs

# Automated tests
python test_api.py test.pdf

# Example client
python examples/api_usage.py
```

---

## 📚 Documentation

- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Setup
- [PHASE1_CHECKLIST.md](PHASE1_CHECKLIST.md) - Testing
- [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) - Costs
- [backend/README.md](backend/README.md) - API docs

---

## 🎯 Next Phases

**Phase 2:** LangGraph agents (Navigator → Professor → Tutor)
**Phase 3:** Next.js frontend with PDF viewer
**Phase 4:** Integration & Polish

---

## 🔑 Key Files

| File                        | Purpose                  |
| --------------------------- | ------------------------ |
| `app/main.py`               | API routes               |
| `app/services/pdf_parser.py`| PDF processing           |
| `app/models/schemas.py`     | Response format          |
| `.env`                      | API keys                 |
| `requirements.txt`          | Dependencies             |

---

## 🚀 Production Checklist

- [ ] Add authentication
- [ ] Enable rate limiting
- [ ] Use PostgreSQL (not SQLite)
- [ ] Move files to S3/MinIO
- [ ] Add monitoring (Sentry)
- [ ] Set up CI/CD
- [ ] Enable HTTPS
- [ ] Add API versioning

---

**Print this page for quick reference!** 📄
