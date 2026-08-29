# AegisAI — Enterprise AI Knowledge & Incident Copilot

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](pyproject.toml)
[![Architecture: Clean](https://img.shields.io/badge/Architecture-Modular%20Monolith-success.svg)](docs/)

AegisAI is a production-grade enterprise AI knowledge and incident copilot engineered for DevOps, SRE, and software engineering teams. It unites hybrid vector/keyword RAG, multi-agent workflows (LangGraph), deep code AST intelligence, Git commit/PR graph tracing, automated incident root-cause analysis (RCA), safe read-only SQL generation, GraphRAG entity-relationship traversal, strict multi-tenancy RBAC, prompt injection defense, comprehensive evaluation, and end-to-end OpenTelemetry/Prometheus/Grafana observability.

---

## Installation

### Prerequisites
- Python 3.11 or 3.12
- Node.js 18+ and npm
- Docker and Docker Compose
- PostgreSQL 16 with pgvector extension

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/aegisai/aegisai.git
cd aegisai

# 2. Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Frontend dependencies
cd frontend && npm install && cd ..

# 5. Configure environment variables
cp example.env .env
```

---

## Build

```bash
# Build backend container image
docker build -t aegisai-backend:latest -f docker/Dockerfile.backend .

# Build frontend Next.js container image
docker build -t aegisai-frontend:latest -f docker/Dockerfile.frontend .

# Build full multi-service stack
docker compose build
```

---

## Run

### Local Docker Compose Deployment
```bash
# Start all infrastructure and microservices in background
docker compose up -d

# Verify service health endpoints
curl http://localhost:8000/health
curl http://localhost:3000/
```

### Local Development Mode
```bash
# Start Backend API Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start Frontend Development Server
cd frontend && npm run dev
```

---

## Dependencies

### Backend & AI Stack
- **FastAPI / Uvicorn**: High-performance asynchronous REST API framework
- **SQLAlchemy 2.0 & asyncpg**: Async ORM and PostgreSQL driver
- **pgvector**: Dense vector similarity search for embeddings
- **Redis & Celery**: Distributed task queue for asynchronous document ingestion
- **MinIO**: S3-compatible blob storage for raw documentation assets
- **OpenTelemetry & Prometheus**: Distributed tracing and 20+ telemetry metrics

### Frontend Stack
- **Next.js 14 (App Router)**: React Server Components & Streaming UI
- **TypeScript**: Static typing across all UI client APIs
- **Tailwind CSS & Lucide Icons**: Responsive enterprise styling

---

## Usage

### 1. Interactive Chat & RAG Knowledge Copilot
Navigate to `http://localhost:3000/chat` to query engineering documentation, architecture specs, and microservice guidelines with SSE streaming and citation grounding.

### 2. Incident Investigation Room (INC-2841)
Navigate to `http://localhost:3000/incidents` to inspect active incidents, correlate deployment drift, and generate automated root cause reports.

### 3. Safe SQL Execution & Schema Explorer
Query databases safely via natural language. The dual-mode AST engine validates read-only queries, enforces strict `LIMIT` caps, and blocks unauthorized DDL/DML.

### 4. Running Automated Tests & Benchmark Suites
```bash
# Run unit and integration tests
pytest -v tests/

# Execute RAG Regression Benchmark Gate
python -m app.evaluation.runner
```

---

## License

Proprietary and Confidential. Proprietary License - Gandhi Komarala. All Rights Reserved.
