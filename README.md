# 🚀 End-to-End RAG Pipeline for AWS & Kubernetes Documentation

An intelligent, context-aware AI chat application that enables users to query complex AWS and Kubernetes documentation using natural language. Built with a modular FastAPI backend, ChromaDB vector storage, Groq Llama 3.1 LLM, and a modern Next.js dark-themed frontend.

## 📸 System Architecture
<img src="./End_To_End_RAG_Pipeline.png" width="500" height="300" />

## ✨ Features

- **Document Ingestion & Chunking**: Automatically processes, splits, and indexes multi-page AWS & Kubernetes PDF whitepapers into manageable chunks using recursive character splitting.
- **Vector Embeddings & Semantic Search**: Generates dense embeddings using `all-MiniLM-L6-v2` and stores them in a persistent ChromaDB vector store using cosine similarity space.
- **Fast & Grounded Context Retrieval**: Fetches top-K relevant document slices with strict relevance thresholding to minimize model hallucinations.
- **High-Speed Inference**: Integrates Groq AI (`llama-3.1-8b-instant`) for lightning-fast, context-grounded response generation.
- **Modern UI/UX**: Dark-mode Next.js chat interface built with Tailwind CSS, featuring automated auto-scrolling, dynamic source tracking, and error resilience.
- **Automated Startup Lifespan**: Intelligent startup hook that checks ChromaDB collection state and auto-ingests documents only when empty.

## 🛠️ Tech Stack

### Backend Layer

- **Language**: Python 3.10+
- **Package Management**: `uv` (Extremely fast Python package installer & resolver)
- **Framework**: FastAPI
- **LLM Integration**: `langchain-groq` (Model: `llama-3.1-8b-instant`)
- **Orchestration**: LangChain
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Database**: ChromaDB (Persistent)

### Frontend Layer

- **Framework**: Next.js (App Router)
- **UI & Styling**: React, Tailwind CSS

## 📂 Project Structure

```
AWS_K8s_RAG_Project/
├── architecture.png              # Root architecture diagram
├── README.md
├── backend/                      # FastAPI Service Layer
│   ├── .env.example              # Template for environment variables
│   ├── pyproject.toml            # Managed by uv
│   ├── data/
│   │   ├── pdf/                  # AWS & Kubernetes PDF files
│   │   └── vector_store/         # Persistent ChromaDB storage
│   └── app/
│       ├── main.py               # FastAPI entry point & CORS
│       ├── routers/
│       │   └── rag_router.py     # Endpoint definition
│       ├── services/
│       │   └── rag_service.py    # Ingestion & generation business logic
│       └── core_utils/
│           ├── create_chunks.py      # PDF processing & text splitting
│           ├── embedding_manager.py  # Sentence Transformers wrapper
│           ├── vector_store.py       # ChromaDB collection wrapper
│           └── rag_retrieval.py      # Top-K document query engine
│
└── frontend/                     # Next.js Application
    ├── package.json
    ├── app/
    │   ├── layout.tsx            # Root layout wrapper
    │   ├── page.tsx              # CloudRAG chat UI
    │   └── globals.css           # Tailwind directives
```

## ⚡ Getting Started

### Prerequisites

- Python 3.10+
- `uv` package manager
- Node.js 18+
- Groq API Key

### 1️⃣ Backend Setup (FastAPI)

Navigate to the backend folder:

```bash
cd backend
```

Configure Environment Variables. Create a `.env` file inside the `backend/` folder:

```
GROQ_RAG_KEY=your_groq_api_key_here
```

Install dependencies using `uv`:

```bash
uv sync
```

Ensure PDFs are placed. Place your target AWS and Kubernetes PDF files into:

```
backend/data/pdf/
```

Run the backend server:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

> ℹ️ Upon first launch, FastAPI's lifespan hook will automatically parse the PDFs in `backend/data/pdf/` and index them into ChromaDB.

### 2️⃣ Frontend Setup (Next.js)

Open a new terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install Node dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Access the chat interface by opening your browser and navigating to [http://localhost:3000](http://localhost:3000).

## 📡 API Reference

### `POST /api/v1/rag/query`

Sends a query to the retrieval pipeline and returns the synthesized answer.

**Request Body:**

```json
{
  "query": "What is an Amazon EC2 instance?",
  "top_k": 3
}
```

**Response Body:**

```json
{
  "query": "What is an Amazon EC2 instance?",
  "answer": "Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud..."
}
```

## 🧠 Key Learnings & AI Concepts Applied

- **Chunking Strategies**: Learned how chunk size (1000 tokens) and overlap (200 tokens) affect semantic boundary preservation during document splitting.
- **Vector Space Mechanics**: Understood cosine distance metrics, indexing strategies, and dimensionality handling (384-dimension dense vectors).
- **RAG System Hygiene**: Implemented prompt engineering techniques to prevent hallucination by strictly constraining the LLM to the provided context window.
- **Decoupled Architecture**: Engineered a production-style separation of concerns between core utility models, business services, API controllers, and frontend view layers.

## 📜 License

This project is open-source and available under the MIT License.
