

# Medical AI Assitant Project

A Medical AI Assitant Project built using **FastAPI**, **LangGraph**, **Groq Llama 3.3**, **Redis**, **Qdrant**, **SQLite**, **PyTorch**, and **Docker**. The system combines conversational AI, Retrieval-Augmented Generation (RAG), medical image analysis, speech processing, and human-in-the-loop validation into a scalable backend architecture.

<p align="left">

<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

<img src="https://img.shields.io/badge/LangGraph-Multi--Agent-blueviolet?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Groq-Llama%203.3-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Qdrant-Vector%20DB-red?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Redis-Cache-red?style=for-the-badge&logo=redis&logoColor=white"/>

<img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>

<img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>

<img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>

<img src="https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>

<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

<img src="https://img.shields.io/badge/WebSocket-Streaming-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/REST-API-informational?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Medical-AI-darkgreen?style=for-the-badge"/>

</p>

---

## Features

- AI-powered medical chatbot
- LangGraph multi-agent orchestration
- Retrieval-Augmented Generation (RAG)
- Medical document search using Qdrant
- Redis semantic and prompt caching
- Medical image segmentation with PyTorch
- Speech-to-Text and Text-to-Speech
- Human-in-the-loop validation
- Background task processing
- REST APIs and WebSocket support
- Dockerized deployment

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| AI Framework | LangGraph |
| LLM | Groq Llama 3.3 |
| Vector Database | Qdrant |
| Database | SQLite |
| Cache | Redis |
| Deep Learning | PyTorch |
| Computer Vision | OpenCV |
| Embeddings | HuggingFace |
| Reranker | Cross Encoder |
| Speech-to-Text | ElevenLabs Scribe |
| Text-to-Speech | Microsoft Edge TTS |
| Containerization | Docker |

---

# Project Structure

```text
medical-ai-backend
│
├── app
│   ├── api
│   ├── agents
│   ├── cache
│   ├── core
│   ├── db
│   ├── rag
│   ├── services
│   ├── vision
│   ├── main.py
│   └── worker.py
│
├── tests
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Architecture

```
Client
   │
   ▼
FastAPI
   │
   ▼
LangGraph Supervisor
   │
   ├────────► Conversation Agent
   ├────────► RAG Agent
   ├────────► Hospital Agent
   ├────────► Financial Agent
   └────────► Vision Agent
                    │
                    ▼
             Redis Background Jobs
                    │
                    ▼
              PyTorch Inference
                    │
                    ▼
              Human Validation
                    │
                    ▼
               Final Response
```

---

# Core Modules

## API

- REST APIs
- WebSockets
- Authentication
- Dependency Injection

---

## LangGraph

- Supervisor Agent
- Conversation Agent
- RAG Agent
- Hospital Agent
- Financial Agent
- Vision Gate

---

## RAG

- Document Loader
- HuggingFace Embeddings
- Qdrant Vector Search
- Cross Encoder Reranker

---

## Vision

- OpenCV Preprocessing
- PyTorch Models
- Segmentation Pipeline
- Background Inference

---

## Speech

- Voice Input
- Speech Recognition
- Text-to-Speech

---

## Database

- SQLite
- Repository Layer
- Audit Logs
- Conversation Storage

---

## Redis

- Prompt Cache
- Semantic Cache
- Background Queue
- Pub/Sub

---

# Request Flow

```text
User

↓

FastAPI

↓

Authentication

↓

LangGraph Supervisor

↓

Selected AI Agent

↓

Redis / SQLite / Qdrant

↓

LLM

↓

Response
```

---

# Vision Pipeline

```text
Medical Image

↓

OpenCV

↓

PyTorch

↓

Segmentation

↓

Confidence Check

↓

Human Review

↓

Final Result
```

---

# RAG Pipeline

```text
User Query

↓

Embeddings

↓

Qdrant Search

↓

Cross Encoder

↓

Context Builder

↓

Groq LLM

↓

Answer
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/sourabhvamdevan/Multimodal-Medical-AI-Assistant-Project.git

cd Multimodal-Medical-AI-Assistant-Project
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

```env
GROQ_API_KEY=

REDIS_URL=

QDRANT_URL=

QDRANT_API_KEY=

DATABASE_URL=sqlite:///medical.db

TAVILY_API_KEY=
```

---

# Run Locally

Start Redis and Qdrant

```bash
docker compose up -d
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Run Worker

```bash
python -m app.worker
```

---

# Docker

Build

```bash
docker build -t medical-ai-backend .
```

Run

```bash
docker compose up
```

---

# API Documentation

After starting the server

```
http://localhost:8000/docs
```

Swagger UI provides interactive API documentation.

---

# Testing

Run all tests

```bash
pytest
```

---

# Future Improvements

- PostgreSQL support
- Kubernetes deployment
- GPU inference server
- Multi-language support
- FHIR integration
- HL7 support
- Medical knowledge graph
- Explainable AI dashboard
- Distributed LangGraph workers

---

# Learning Outcomes

This project demonstrates practical implementation of:

- FastAPI
- LangGraph
- Multi-Agent Systems
- Retrieval-Augmented Generation (RAG)
- Redis
- SQLite
- Qdrant
- PyTorch
- OpenCV
- Docker
- Background Job Processing
- Speech AI
- Medical AI Backend Development

---

# License

This project is intended for educational and research purposes.

---

# Author

**Sourabh V**

Medical AI Backend

FastAPI • LangGraph • Redis • Qdrant • SQLite • PyTorch • Docker