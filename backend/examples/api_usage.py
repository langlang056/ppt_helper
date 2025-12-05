"""
Example usage of UniTutor AI Backend API.

This script demonstrates how to:
1. Upload a PDF
2. Get explanations for specific pages
3. Handle caching
4. Retrieve PDF metadata
"""

import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
PDF_PATH = "path/to/your/lecture.pdf"  # Change this!


def upload_pdf(pdf_path: str) -> dict:
    """Upload a PDF and get its ID."""
    print(f"📤 Uploading: {pdf_path}")

    with open(pdf_path, "rb") as f:
        files = {"file": (Path(pdf_path).name, f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)

    response.raise_for_status()
    data = response.json()

    print(f"✅ Uploaded successfully!")
    print(f"   PDF ID: {data['pdf_id']}")
    print(f"   Pages: {data['total_pages']}")
    print(f"   Message: {data['message']}\n")

    return data


def get_explanation(pdf_id: str, page_number: int) -> dict:
    """Get AI explanation for a specific page."""
    print(f"🤖 Fetching explanation for page {page_number}...")

    response = requests.get(f"{BASE_URL}/api/explain/{pdf_id}/{page_number}")
    response.raise_for_status()

    data = response.json()

    print(f"✅ Explanation retrieved!")
    print(f"   Type: {data['page_type']}")
    print(f"   Summary: {data['content']['summary']}")
    print(f"   Key Points: {len(data['content']['key_points'])}\n")

    return data


def get_pdf_info(pdf_id: str) -> dict:
    """Get PDF metadata."""
    print(f"ℹ️  Fetching PDF info...")

    response = requests.get(f"{BASE_URL}/api/pdf/{pdf_id}/info")
    response.raise_for_status()

    data = response.json()

    print(f"✅ PDF Info:")
    print(f"   Filename: {data['filename']}")
    print(f"   Total Pages: {data['total_pages']}")
    print(f"   Uploaded: {data['uploaded_at']}\n")

    return data


def demo_workflow():
    """Demonstrate a typical workflow."""
    print("=" * 60)
    print("UniTutor AI - API Usage Example")
    print("=" * 60)
    print()

    # 1. Upload PDF
    result = upload_pdf(PDF_PATH)
    pdf_id = result["pdf_id"]
    total_pages = result["total_pages"]

    # 2. Get PDF info
    get_pdf_info(pdf_id)

    # 3. Get explanation for first page
    page1 = get_explanation(pdf_id, 1)

    # Save to file
    with open("page1_explanation.json", "w", encoding="utf-8") as f:
        json.dump(page1, f, indent=2, ensure_ascii=False)
    print("💾 Saved to page1_explanation.json\n")

    # 4. Get explanation for last page
    if total_pages > 1:
        last_page = get_explanation(pdf_id, total_pages)

    # 5. Upload same PDF again (should hit cache)
    print("🔄 Uploading same PDF again (testing cache)...")
    result2 = upload_pdf(PDF_PATH)

    if result2["pdf_id"] == pdf_id:
        print("✅ Cache hit! Same PDF ID returned.\n")

    # 6. Demonstrate that 2nd request is instant (cached)
    print("⚡ Fetching page 1 again (should be instant)...")
    import time

    start = time.time()
    get_explanation(pdf_id, 1)
    elapsed = time.time() - start

    print(f"⏱️  Response time: {elapsed:.3f} seconds (cached!)\n")

    print("=" * 60)
    print("✅ Demo completed successfully!")
    print("=" * 60)


def batch_process_all_pages(pdf_id: str, total_pages: int):
    """Process all pages and save explanations."""
    print(f"📚 Batch processing {total_pages} pages...\n")

    explanations = []

    for page_num in range(1, total_pages + 1):
        try:
            explanation = get_explanation(pdf_id, page_num)
            explanations.append(explanation)
            print(f"   ✓ Page {page_num}/{total_pages}")
        except Exception as e:
            print(f"   ✗ Page {page_num} failed: {e}")

    # Save all explanations
    output_file = f"all_explanations_{pdf_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(explanations, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved all explanations to {output_file}")


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(BASE_URL)
        if response.json()["status"] != "healthy":
            print("❌ Server is not healthy!")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Make sure server is running: python -m uvicorn app.main:app --reload")
        exit(1)

    # Check if PDF path is provided
    if PDF_PATH == "path/to/your/lecture.pdf":
        print("❌ Please set PDF_PATH in the script first!")
        print("   Edit line 13: PDF_PATH = 'your/actual/path.pdf'")
        exit(1)

    # Run demo
    demo_workflow()

    # Optional: Uncomment to batch process all pages
    # result = upload_pdf(PDF_PATH)
    # batch_process_all_pages(result['pdf_id'], result['total_pages'])
