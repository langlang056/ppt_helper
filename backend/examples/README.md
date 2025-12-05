# API Usage Examples

This folder contains example scripts demonstrating how to interact with the UniTutor AI backend.

## 📝 Available Examples

### 1. `api_usage.py` - Complete Workflow Demo

Demonstrates:
- Uploading a PDF
- Getting explanations for specific pages
- Checking cache behavior
- Batch processing all pages
- Saving results to JSON

**Usage:**
```bash
# Edit the script to set your PDF path
nano api_usage.py  # Change line 13

# Run the demo
python api_usage.py
```

**Output:**
- Console logs showing each step
- `page1_explanation.json` - First page explanation
- `all_explanations_{pdf_id}.json` - All pages (if batch mode enabled)

---

## 🔧 Using the Examples

### Prerequisites

Make sure the backend server is running:
```bash
cd ../
python -m uvicorn app.main:app --reload
```

### Install requests library (if needed):
```bash
pip install requests
```

---

## 📚 More Examples

### Quick Upload

```python
import requests

with open("lecture.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": f}
    )

print(response.json())
# Output: {"pdf_id": "...", "total_pages": 10, ...}
```

### Get Single Page

```python
import requests

pdf_id = "a1b2c3d4e5f6g7h8"  # From upload response
page_num = 5

response = requests.get(
    f"http://localhost:8000/api/explain/{pdf_id}/{page_num}"
)

explanation = response.json()
print(explanation["content"]["summary"])
```

### Check if PDF Exists

```python
import requests

pdf_id = "a1b2c3d4e5f6g7h8"

try:
    response = requests.get(f"http://localhost:8000/api/pdf/{pdf_id}/info")
    print(f"PDF exists: {response.json()['filename']}")
except requests.exceptions.HTTPError:
    print("PDF not found")
```

---

## 🧪 Testing with cURL

### Upload
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@test.pdf"
```

### Get Explanation
```bash
curl "http://localhost:8000/api/explain/a1b2c3d4e5f6g7h8/1"
```

### Get PDF Info
```bash
curl "http://localhost:8000/api/pdf/a1b2c3d4e5f6g7h8/info"
```

---

## 🎯 Next Steps

Once you're comfortable with Phase 1 API:

1. **Phase 2:** We'll enhance these explanations with AI agents
2. **Phase 3:** Frontend will consume these APIs
3. You can build your own clients (mobile app, CLI, etc.)

---

## 💡 Tips

1. **API Keys in Production:**
   - Never hardcode API keys
   - Use environment variables
   - Implement authentication

2. **Error Handling:**
   - Always use `try/except` for network requests
   - Check `response.status_code` before processing
   - Log errors for debugging

3. **Performance:**
   - Cache responses on client side
   - Use batch processing for multiple pages
   - Implement rate limiting for production

---

**Need help?** Check the main [backend README](../README.md) or [QUICKSTART guide](../../QUICKSTART.md)
