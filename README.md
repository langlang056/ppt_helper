# UniTutor AI - Multi-Agent Courseware Explainer

An intelligent teaching assistant that transforms university lecture slides into accessible explanations using AI agents.

## 🎯 Project Overview

**Problem:** Students struggle to understand complex academic slides (especially in foreign languages like French/English).

**Solution:** Upload a PDF courseware → AI agents extract concepts, provide Chinese explanations with analogies.

**UX:** Split-screen interface - Original PDF on the left, AI explanations on the right.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (Next.js 14)              │
│  ┌─────────────────┐  ┌────────────────────┐   │
│  │  PDF Viewer     │  │  Explanation Panel │   │
│  │  (react-pdf)    │  │  (Shadcn/UI Cards) │   │
│  └─────────────────┘  └────────────────────┘   │
└──────────────┬──────────────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────────────┐
│           Backend (FastAPI + LangGraph)         │
│  ┌──────────────────────────────────────────┐   │
│  │  LangGraph Agent Workflow                │   │
│  │  Navigator → Professor → Tutor → Format  │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐    │
│  │ LlamaParse │  │  Claude   │  │  SQLite    │    │
│  │ (PDF Parse)│  │  3.5 LLM  │  │  (Cache)   │    │
│  └──────────┘  └──────────┘  └────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

| Layer         | Technology                           |
| ------------- | ------------------------------------ |
| **Frontend**  | Next.js 14, TypeScript, Tailwind CSS |
| **PDF Viewer**| react-pdf                            |
| **Backend**   | FastAPI, Python 3.11+                |
| **Agents**    | LangChain + LangGraph                |
| **LLM**       | Claude 3.5 Sonnet (Anthropic)        |
| **PDF Parser**| LlamaParse (by LlamaIndex)           |
| **Database**  | SQLite (local), PostgreSQL (prod)    |
| **State Mgmt**| Zustand                              |

---

## 🚀 Implementation Phases

### ✅ Phase 1: Backend Parsing & Basic API (COMPLETED)

**What's Done:**
- FastAPI server with CORS support
- PDF upload with duplicate detection (SHA256 hashing)
- LlamaParse integration for text extraction
- SQLite caching to save costs
- Basic REST API (`/upload`, `/explain/{pdf_id}/{page_number}`)

**Test It:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Add your API keys to .env
python -m uvicorn app.main:app --reload
```

See [backend/README.md](backend/README.md) for detailed instructions.

---

### 🔄 Phase 2: LangGraph Multi-Agent Workflow (NEXT)

**Goals:**
1. Build **Navigator Agent** - Classify page type (TITLE/CONTENT/END)
2. Build **Professor Agent** - Extract academic facts in original language
3. Build **Tutor Agent** - Simplify to Chinese + create analogy
4. Build **Formatter Agent** - Structure output as JSON

**Agent Flow:**
```
Input: Page Text (French/English)
  ↓
Navigator → Is this TITLE or CONTENT?
  ↓
Professor → Extract: "Gradient Descent: ∇f(x) = ..."
  ↓
Tutor → "梯度下降就像蒙眼下山,每次往最陡的方向走一小步"
  ↓
Formatter → JSON Output
```

**Implementation Plan:**
- Create `backend/app/agents/graph.py` (LangGraph state machine)
- Create individual agent nodes with Claude prompts
- Integrate into `/explain` endpoint
- Test with real lecture PDFs

---

### 🎨 Phase 3: Frontend Setup & PDF Viewer

**Goals:**
- Initialize Next.js 14 with App Router
- Setup Shadcn/UI components
- Implement split-screen layout
- Integrate `react-pdf` for PDF rendering
- Add page navigation (Next/Prev buttons)
- Sync state between PDF viewer and explanation panel

**Key Features:**
- Responsive design (desktop-first, mobile-friendly)
- Loading states with skeleton UI
- Error handling with toast notifications
- Preloading N+1, N+2 pages for smooth UX

---

### 🔗 Phase 4: Integration & Polish

**Goals:**
- Connect frontend to backend API
- Implement Zustand state management
- Add upload progress indicator
- Render AI explanations beautifully (Cards, Badges, Syntax highlighting)
- Add "Regenerate" button for bad explanations
- Performance optimization (lazy loading, virtualization)

---

## 💰 Cost Estimation

**Your Usage:** 2 users/day × 2.5 PDFs × 50 pages = 250 pages/day

| Service       | Cost/Page | Daily Cost | Monthly Cost |
| ------------- | --------- | ---------- | ------------ |
| LlamaParse    | $0.003    | $0.75      | $22.50       |
| Claude API    | ~$0.02    | $5.00      | $150.00      |
| **Total**     |           | **~$6**    | **~$180**    |

**Caching Impact:** 2nd access to same PDF = $0 (served from SQLite)

---

## 🔑 Setup Requirements

### 1. Get API Keys

**LlamaParse (Required for Phase 1):**
1. Go to [https://cloud.llamaindex.ai/](https://cloud.llamaindex.ai/)
2. Sign up and create API key
3. Copy key starting with `llx-...`

**Anthropic Claude (Required for Phase 2):**
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Get API key starting with `sk-ant-...`
3. Add credits ($5 minimum)

### 2. Environment Variables

Create `backend/.env`:
```env
LLAMA_CLOUD_API_KEY=llx-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 📂 Project Structure

```
ppt_helper/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI routes
│   │   ├── config.py            # Settings
│   │   ├── agents/              # (Phase 2) LangGraph nodes
│   │   ├── models/
│   │   │   ├── database.py      # SQLAlchemy models
│   │   │   └── schemas.py       # API schemas
│   │   └── services/
│   │       ├── pdf_parser.py    # LlamaParse wrapper
│   │       └── cache_service.py # DB caching
│   ├── uploads/                 # Stored PDFs
│   ├── requirements.txt
│   └── .env
│
└── frontend/                    # (Phase 3) Next.js app
    ├── app/
    ├── components/
    └── package.json
```

---

## 🧪 Testing Phase 1

```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Run tests
python test_api.py path/to/test.pdf
```

**Expected Output:**
```
✅ Server status: healthy
✅ Upload successful!
   PDF ID: a3f2d9c8b1e4f5a6
   Total Pages: 42
✅ Explanation retrieved!
```

---

## 🎓 Design Highlights

### Why LlamaParse?
- Handles complex slide layouts (multi-column, tables, diagrams)
- Better than PyPDF2/pdfplumber for academic materials
- Outputs structured Markdown

### Why LangGraph?
- Clean state machine for agent workflows
- Better than basic LangChain chains for multi-agent systems
- Built-in checkpointing and debugging

### Why Caching?
- Same PDF uploaded twice = instant response
- Saves ~$0.02/page on repeated access
- Essential for 2-user scenario (likely reviewing same materials)

---

## 📋 Next Steps

**Ready to proceed with Phase 2?** Let me know and I'll implement the LangGraph agent workflow with these features:

1. **Navigator Agent** with page classification
2. **Professor Agent** for academic extraction
3. **Tutor Agent** for Chinese explanations + analogies
4. Full integration with Claude 3.5 Sonnet

**Or want to jump to Phase 3?** I can start the Next.js frontend setup.

---

## 🤝 Contributing

This is a personal project. Feedback welcome!

## 📄 License

Private use only.

---

**Built with Claude Code** 🤖
