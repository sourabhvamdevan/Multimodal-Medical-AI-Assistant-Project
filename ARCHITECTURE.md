# Overall System Architecture

```text
                           USER
                             │
                             ▼
                  Web / Mobile Application
                             │
                             ▼
                     FastAPI API Gateway
                             │
       ┌─────────────────────┼──────────────────────┐
       │                     │                      │
       ▼                     ▼                      ▼
   Chat API             Vision API          Human Review API
       │                     │                      │
       └──────────────┬──────┴──────────────┬───────┘
                      │
                      ▼
              LangGraph Supervisor
                      │
      ┌───────────────┼────────────────────────────────────┐
      ▼               ▼               ▼                    ▼
Conversation      RAG Agent      Hospital Agent     Financial Agent
     │               │               │                    │
     │               │               │                    │
     │         Medical Search        │                    │
     │               │               │                    │
     │               ▼               │                    │
     │      HuggingFace Embeddings   │                    │
     │               │               │                    │
     │               ▼               │                    │
     │         Qdrant Vector DB      │                    │
     │               │               │                    │
     └───────────────┴───────────────┴────────────────────┘
                      │
                      ▼
               Final AI Response
                      │
                      ▼
                  FastAPI Response
                      │
                      ▼
                     Client
```

---

# Vision Processing Architecture

```text
Medical Image
      │
      ▼
Image Upload API
      │
      ▼
Redis Queue
      │
      ▼
Background Worker
      │
      ▼
OpenCV Preprocessing
      │
      ▼
ROI Extraction
      │
      ▼
Normalization
      │
      ▼
PyTorch Model
      │
      ▼
Segmentation Mask
      │
      ▼
Measurements
      │
      ▼
Confidence Check
      │
      ▼
Vision Gate
      │
 ┌────┴─────┐
 │          │
 ▼          ▼
High      Low
 │          │
 ▼          ▼
Response  Human Review
 │          │
 └────┬─────┘
      ▼
 Final Result
```

---

# RAG Architecture

```text
User Query
     │
     ▼
Embedding Generator
     │
     ▼
Qdrant Search
     │
     ▼
Top-K Chunks
     │
     ▼
Cross Encoder
     │
     ▼
Re-ranked Context
     │
     ▼
LangGraph RAG Agent
     │
     ▼
Groq Llama 3.3
     │
     ▼
Answer
```

---

# Redis Architecture

```text
                  Redis
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Prompt Cache   Background Queue   Pub/Sub
     │              │              │
     ▼              ▼              ▼
 Faster LLM     Vision Worker   Live Updates
 Responses      Audio Worker    Notifications
                PDF Worker
```

---

# Database Architecture

```text
               SQLite
                  │
      ┌───────────┼─────────────┐
      ▼           ▼             ▼
 Conversation  Validation   Audit Logs
    Threads      Records
      │
      ▼
 Repository Layer
      │
      ▼
 LangGraph Agents
```

---

# Speech Pipeline

```text
Voice Input
      │
      ▼
ElevenLabs Scribe
      │
      ▼
Speech to Text
      │
      ▼
LangGraph
      │
      ▼
Generated Response
      │
      ▼
Edge TTS
      │
      ▼
Voice Output
```

---

# Complete Request Flow

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Authentication
   │
   ▼
Supervisor Agent
   │
   ├──────────────► Conversation
   │
   ├──────────────► RAG
   │                    │
   │                    ▼
   │                Qdrant
   │
   ├──────────────► Hospital
   │
   ├──────────────► Financial
   │
   └──────────────► Vision
                         │
                         ▼
                    Redis Queue
                         │
                         ▼
                    Background Worker
                         │
                         ▼
                   PyTorch Inference
                         │
                         ▼
                  Human Validation
                         │
                         ▼
                  Final AI Response
                         │
                         ▼
                      Client
```