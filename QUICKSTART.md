# 🚀 Quick Start Guide - UniTutor AI

Get your backend running in **5 minutes**!

---

## Step 1: Get Your API Key (2 minutes)

1. **Sign up for LlamaParse:**
   - Go to [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/)
   - Create account (GitHub login works)
   - Click "API Keys" → "Create API Key"
   - Copy the key (starts with `llx-...`)

2. **Save it:** Write it down, you'll need it in Step 3

---

## Step 2: Install Backend (1 minute)

Open terminal in the project folder:

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Wait 1-2 minutes** for installation to complete.

---

## Step 3: Configure API Key (30 seconds)

```bash
# Copy example config
cp .env.example .env

# Edit .env file (use any text editor)
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Paste your LlamaParse API key:**
```env
LLAMA_CLOUD_API_KEY=llx-paste-your-key-here
ANTHROPIC_API_KEY=sk-ant-leave-this-for-phase2
```

Save and close.

---

## Step 4: Start Server (10 seconds)

### Option A: Use start script (Windows)
```bash
start.bat
```

### Option B: Manual start (All platforms)
```bash
python -m uvicorn app.main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Database initialized
✅ Upload directory: uploads
```

---

## Step 5: Test It! (1 minute)

### Open your browser:
[http://localhost:8000/docs](http://localhost:8000/docs)

You'll see the **interactive API documentation**.

### Try uploading a PDF:

1. Click on **POST /api/upload** (the green section)
2. Click **"Try it out"**
3. Click **"Choose File"** and select any PDF
4. Click **"Execute"**

**Expected result:**
```json
{
  "pdf_id": "a1b2c3d4e5f6g7h8",
  "total_pages": 10,
  "filename": "your-file.pdf",
  "message": "PDF uploaded and parsed successfully"
}
```

### Get explanation for page 1:

1. Copy the `pdf_id` from the upload response
2. Click on **GET /api/explain/{pdf_id}/{page_number}**
3. Click **"Try it out"**
4. Paste the `pdf_id` and enter `1` for page_number
5. Click **"Execute"**

**You'll see extracted text from the PDF!**

---

## ✅ Success!

Your Phase 1 backend is now running.

**Next steps:**
- Check [PHASE1_CHECKLIST.md](PHASE1_CHECKLIST.md) for detailed testing
- Read [backend/README.md](backend/README.md) for API documentation
- When ready, ask me to implement **Phase 2 (LangGraph Agents)**

---

## 🐛 Common Issues

### "Cannot find module uvicorn"
**Fix:** Make sure virtual environment is activated (you should see `(venv)` in terminal)

### "LLAMA_CLOUD_API_KEY not found"
**Fix:** Check that `.env` file exists and contains your key (no spaces around `=`)

### "Connection refused" when accessing http://localhost:8000
**Fix:** Make sure server is running. Check terminal for errors.

### PDF upload fails
**Fix:**
- Check file is a valid PDF
- File size must be < 50MB
- PDF must not be password-protected

---

## 📊 What Just Happened?

1. ✅ FastAPI server started on port 8000
2. ✅ SQLite database created (`unitutor.db`)
3. ✅ Upload folder created (`uploads/`)
4. ✅ LlamaParse integrated for PDF parsing
5. ✅ Caching system ready

**Your backend can now:**
- Accept PDF uploads
- Parse complex slides with LlamaParse
- Cache results to save costs
- Serve via REST API

**Phase 2 will add:**
- AI agents (Navigator, Professor, Tutor)
- Claude 3.5 for explanations in Chinese
- Analogy generation

---

**Need help?** Check the detailed [README.md](README.md) or [PHASE1_CHECKLIST.md](PHASE1_CHECKLIST.md)
