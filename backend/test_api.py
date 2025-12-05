"""Quick test script for the FastAPI backend."""
import requests
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"


def test_health():
    """Test server health."""
    print("🔍 Testing server health...")
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Server status: {response.json()['status']}")
    print()


def test_upload(pdf_path: str):
    """Test PDF upload."""
    print(f"📤 Uploading PDF: {pdf_path}")

    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)

    with open(pdf_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/upload", files={"file": ("test.pdf", f, "application/pdf")}
        )

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        sys.exit(1)

    data = response.json()
    print(f"✅ Upload successful!")
    print(f"   PDF ID: {data['pdf_id']}")
    print(f"   Total Pages: {data['total_pages']}")
    print(f"   Message: {data['message']}")
    print()

    return data["pdf_id"], data["total_pages"]


def test_explanation(pdf_id: str, page_number: int):
    """Test explanation endpoint."""
    print(f"🤖 Getting explanation for page {page_number}...")

    response = requests.get(f"{BASE_URL}/api/explain/{pdf_id}/{page_number}")

    if response.status_code != 200:
        print(f"❌ Failed: {response.text}")
        sys.exit(1)

    data = response.json()
    print(f"✅ Explanation retrieved!")
    print(f"   Page Type: {data['page_type']}")
    print(f"   Summary: {data['content']['summary']}")
    print(f"   Key Points: {len(data['content']['key_points'])}")
    print()

    return data


def test_pdf_info(pdf_id: str):
    """Test PDF info endpoint."""
    print(f"ℹ️  Getting PDF info...")

    response = requests.get(f"{BASE_URL}/api/pdf/{pdf_id}/info")

    if response.status_code != 200:
        print(f"❌ Failed: {response.text}")
        sys.exit(1)

    data = response.json()
    print(f"✅ PDF Info:")
    print(f"   Filename: {data['filename']}")
    print(f"   Total Pages: {data['total_pages']}")
    print(f"   Uploaded: {data['uploaded_at']}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("UniTutor AI - Backend Test Suite (Phase 1)")
    print("=" * 60)
    print()

    # Check if server is running
    try:
        test_health()
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("   Start it with: python -m uvicorn app.main:app --reload")
        sys.exit(1)

    # Get PDF path from command line or use default
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("Usage: python test_api.py <path_to_pdf>")
        print("Example: python test_api.py ../test_lecture.pdf")
        sys.exit(1)

    # Run tests
    pdf_id, total_pages = test_upload(pdf_path)
    test_pdf_info(pdf_id)

    # Test first page
    test_explanation(pdf_id, 1)

    # Test last page
    if total_pages > 1:
        test_explanation(pdf_id, total_pages)

    print("=" * 60)
    print("✅ All tests passed! Phase 1 backend is working correctly.")
    print("=" * 60)
