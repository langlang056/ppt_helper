# Phase 1 Completion Checklist

Use this checklist to verify that Phase 1 backend is working correctly before moving to Phase 2.

## 📋 Pre-Installation Checks

- [ ] Python 3.11+ installed (`python --version`)
- [ ] LlamaCloud account created at [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/)
- [ ] LlamaParse API key obtained (starts with `llx-`)
- [ ] Test PDF file prepared (5-10 pages, academic content, French/English)

---

## 🔧 Installation Steps

### 1. Setup Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

- [ ] Virtual environment created successfully
- [ ] Virtual environment activated (you should see `(venv)` in terminal)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

- [ ] All packages installed without errors
- [ ] No version conflicts reported

**Common Issues:**
- If `llama-parse` fails: Upgrade pip with `pip install --upgrade pip`
- If `aiosqlite` fails on Windows: Install Visual C++ Build Tools

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

- [ ] `.env` file created
- [ ] `LLAMA_CLOUD_API_KEY` filled in
- [ ] `ANTHROPIC_API_KEY` added (optional for Phase 1, required for Phase 2)

---

## 🚀 Running the Server

### Start the server:

```bash
# Option 1: Direct command
python -m uvicorn app.main:app --reload

# Option 2: Use start script (Windows)
start.bat
```

- [ ] Server starts without errors
- [ ] You see: `Uvicorn running on http://0.0.0.0:8000`
- [ ] You see: `✅ Database initialized`
- [ ] You see: `✅ Upload directory: uploads`

### Verify Server Health

Open browser to [http://localhost:8000](http://localhost:8000)

**Expected Response:**
```json
{
  "message": "UniTutor AI Backend is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

- [ ] Health check endpoint returns JSON
- [ ] Status is "healthy"

---

## 🧪 Testing API Endpoints

### Test 1: Upload PDF

**Using the interactive docs** (easiest method):
1. Go to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Expand `POST /api/upload`
3. Click "Try it out"
4. Upload a test PDF
5. Click "Execute"

**Expected Response:**
```json
{
  "pdf_id": "a1b2c3d4e5f6g7h8",
  "total_pages": 10,
  "filename": "test_lecture.pdf",
  "message": "PDF uploaded and parsed successfully"
}
```

- [ ] Upload returns 200 OK status
- [ ] `pdf_id` is a 16-character hex string
- [ ] `total_pages` matches your PDF
- [ ] File appears in `backend/uploads/` directory

**Using test script:**
```bash
python test_api.py path/to/your/test.pdf
```

- [ ] All tests pass
- [ ] No errors in console

### Test 2: Get Page Explanation

**Using the interactive docs:**
1. Go to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Expand `GET /api/explain/{pdf_id}/{page_number}`
3. Enter the `pdf_id` from Test 1
4. Enter page number: `1`
5. Click "Execute"

**Expected Response:**
```json
{
  "page_number": 1,
  "page_type": "CONTENT",
  "content": {
    "summary": "第 1 页内容(待 AI 处理)",
    "key_points": [
      {
        "concept": "原始文本",
        "explanation": "Some extracted text...",
        "is_important": false
      }
    ],
    "analogy": "[将在 Phase 2 添加 LangGraph 处理]",
    "example": ""
  }
}
```

- [ ] Returns 200 OK
- [ ] `page_number` matches request
- [ ] `key_points[0].explanation` contains actual text from PDF
- [ ] Response is cached (2nd request is instant)

### Test 3: Get PDF Info

**Using the interactive docs:**
1. `GET /api/pdf/{pdf_id}/info`
2. Enter your `pdf_id`

**Expected Response:**
```json
{
  "pdf_id": "a1b2c3d4e5f6g7h8",
  "filename": "test_lecture.pdf",
  "total_pages": 10,
  "uploaded_at": "2025-01-15T10:30:00.123456"
}
```

- [ ] Returns PDF metadata correctly
- [ ] `uploaded_at` is a valid ISO timestamp

### Test 4: Upload Same PDF Again (Deduplication)

Upload the exact same PDF file again.

**Expected Response:**
```json
{
  "pdf_id": "a1b2c3d4e5f6g7h8",  // Same ID!
  "total_pages": 10,
  "filename": "test_lecture.pdf",
  "message": "PDF already exists in cache"  // Notice the message
}
```

- [ ] Returns same `pdf_id`
- [ ] Message says "already exists in cache"
- [ ] No duplicate file created in `uploads/` folder

---

## 🗄️ Database Verification

Check that SQLite database was created:

```bash
# Should see unitutor.db file
ls -la unitutor.db   # Linux/Mac
dir unitutor.db      # Windows
```

- [ ] `unitutor.db` file exists
- [ ] File size > 0 bytes

**Optional: Inspect database** (requires SQLite CLI):
```bash
sqlite3 unitutor.db
sqlite> .tables
# Should show: pdf_documents, page_explanations
sqlite> SELECT * FROM pdf_documents;
sqlite> .quit
```

- [ ] `pdf_documents` table exists
- [ ] `page_explanations` table exists
- [ ] Your uploaded PDF appears in `pdf_documents`

---

## 🔍 LlamaParse Verification

### Check Parse Quality

1. Upload a complex PDF (with tables, multi-column layout)
2. Get explanation for a page with tables
3. Check if `explanation` contains structured text (not garbled)

**Good Parse Example:**
```
| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |
```

**Bad Parse Example (switch to PyPDF2 if you see this):**
```
H e a d e r 1 H e a d e r 2 D a t a 1 D a t a 2
```

- [ ] Tables are preserved in markdown format
- [ ] Multi-column text flows correctly
- [ ] Formulas/equations are readable

---

## 🐛 Troubleshooting

### Problem: "LLAMA_CLOUD_API_KEY not found"

**Solution:**
1. Check `.env` file exists in `backend/` directory
2. Open `.env` and verify key format: `LLAMA_CLOUD_API_KEY=llx-...`
3. Restart server after editing `.env`

---

### Problem: "Failed to parse PDF"

**Possible Causes:**
1. PDF is password-protected → Remove password
2. PDF is > 50MB → Reduce file size or increase `max_file_size_mb` in `config.py`
3. LlamaParse API quota exceeded → Check usage at [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/)

**Debug Steps:**
```python
# Test LlamaParse directly
from llama_parse import LlamaParse
parser = LlamaParse(api_key="your-key", result_type="markdown")
docs = parser.load_data("test.pdf")
print(docs[0].text)
```

---

### Problem: "Database locked" error

**Solution:**
```bash
# Delete database and restart
rm unitutor.db      # Linux/Mac
del unitutor.db     # Windows

# Restart server (database will be recreated)
```

---

### Problem: Upload works but explanation is empty

**Cause:** LlamaParse returned empty text for that page (blank slide)

**Verify:**
```bash
# Check server logs for LlamaParse output
# Should see "Parsing PDF..." messages
```

---

## ✅ Phase 1 Success Criteria

All of these must pass before proceeding to Phase 2:

- [x] Server starts without errors
- [x] Health check returns "healthy"
- [x] PDF upload works and returns `pdf_id`
- [x] Duplicate upload returns same `pdf_id`
- [x] Page explanation returns extracted text
- [x] Cache works (2nd request is faster)
- [x] Database contains uploaded PDF metadata
- [x] LlamaParse correctly extracts text from complex slides

---

## 📊 Performance Benchmarks

Record these numbers for comparison:

| Metric                    | Your Result | Expected  |
| ------------------------- | ----------- | --------- |
| Upload time (10-page PDF) | _____ sec   | 5-15 sec  |
| First page parse          | _____ sec   | 3-8 sec   |
| Cached page retrieval     | _____ sec   | < 0.5 sec |
| Database size (1 PDF)     | _____ KB    | 50-200 KB |

---

## 🎉 Next Steps

Once all checks pass:

1. **Proceed to Phase 2:** LangGraph Agent Implementation
   - I'll create the Navigator, Professor, Tutor agents
   - Integrate Claude 3.5 Sonnet for explanations
   - Generate structured Chinese output with analogies

2. **Or Jump to Phase 3:** Frontend Setup
   - Initialize Next.js project
   - Build split-screen PDF viewer
   - Connect to backend API

**Which phase would you like to tackle next?**

---

## 📝 Notes

Use this space to record any issues or observations:

```
Date: ___________
Issues encountered:


Solutions applied:


Performance notes:


```
