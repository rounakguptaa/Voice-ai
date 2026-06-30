# GuruAI: Voice-Enabled AI Teaching Assistant

GuruAI is a full-stack, voice-enabled teaching assistant designed specifically for **Class 10 Science and Mathematics** on Haryana government school smart boards. It provides Hinglish responses, audio explanations, dark-mode concept visuals, and interactive quizzes.

---

## 📂 Project Structure

```text
GuruAI/
├── ncert_chunks.json           # Combined NCERT Class 10 Science and Maths text chunks
├── requirements.txt            # System dependencies
├── README.md                   # System documentation
├── .gitignore                  # Excluded folders (e.g. caches, env keys)
├── backend.Dockerfile          # Docker configuration for Railway (FastAPI backend)
├── frontend.Dockerfile         # Docker configuration for Railway (Streamlit frontend)
├── backend/
│   ├── __init__.py
│   ├── config.py               # Path mapping, chunk loaders, and fallback topics
│   ├── build_indexes.py        # Vector embedding script (run once)
│   ├── guardrails.py           # FAISS-based relevance filter (threshold = 0.7)
│   ├── rag_engine.py           # RAG retrieval module
│   ├── agents.py               # Subject-specific Hinglish response generators
│   ├── stt_handler.py          # Speech-To-Text transcription using OpenAI Whisper
│   ├── tts_handler.py          # Microsoft Neural voice TTS with gTTS fallback
│   ├── visual_generator.py     # Matplotlib dark-mode summary card builder
│   ├── quiz_generator.py       # Template-based MCQ generator
│   └── main.py                 # FastAPI application (using dynamic request URLs)
├── frontend/
│   └── streamlit_app.py        # Streamlit classroom smart board interface (reads BACKEND_URL)
├── syllabus_data/
│   └── indexes/                # Pre-built FAISS databases and metadata pickles
└── temp_audio/                 # Ephemeral folder for cached TTS speech files (gitignored)
```

---

## 🛠️ Local Installation & Setup

### 1. Install Dependencies
Ensure you have Python 3.11+ installed. Run the following command from the project root directory:
```bash
pip install -r requirements.txt
```

### 2. Build the FAISS Vector Stores
Run the build script once to embed and index the NCERT textbook chunks:
```bash
python -m backend.build_indexes
```
*Note: This will download the `all-MiniLM-L6-v2` SentenceTransformer model (approx. 120MB) and generate Science and Mathematics vectors.*

### 3. Create Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run Locally
We run both backend and frontend applications simultaneously:

* **Start the FastAPI Backend**:
  ```bash
  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```
  The backend API documentation is accessible at `http://localhost:8000/docs`.

* **Start the Streamlit Frontend**:
  In a new terminal window, run:
  ```bash
  python -m streamlit run frontend/streamlit_app.py --server.port 8501
  ```
  Open `http://localhost:8501` in your browser.

---

## ☁️ Deployment Guide (Railway)

We host both the FastAPI backend and Streamlit frontend services on **Railway** using separate services built from the same GitHub repository. 

> [!NOTE]
> **Why not deploy Streamlit on Vercel?** 
> Vercel is designed for serverless execution (stateless, short-lived functions). Streamlit requires a persistent, long-running Python server to maintain UI state and handle WebSocket connections. Deploying Streamlit on Vercel is not natively supported.

### Step 1: Connect your Git Repository
1. Create a repository on GitHub (e.g., `guru-ai-teaching-assistant`).
2. Push your local files to GitHub (sensitive environment files `.env` and temporary audio files are automatically excluded by `.gitignore`):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ready for Railway deployment"
   git remote add origin https://github.com/your-username/your-repo.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy the Backend on Railway
1. Go to [Railway.app](https://railway.app) and log in.
2. Click **New Project** -> **Deploy from GitHub repo** and select your repository.
3. Once the service is created, go to the service **Settings** -> **General** and change the service name to `guruai-backend`.
4. Under **Settings** -> **Build**, set:
   * **Dockerfile Path**: `backend.Dockerfile`
5. Go to the **Variables** tab and add:
   * `GROQ_API_KEY` = *[Your Groq API Key]*
6. Go to **Settings** -> **Networking** and click **Generate Domain** (e.g., `https://guruai-backend-production.up.railway.app`). Write this URL down.

### Step 3: Deploy the Frontend on Railway
1. Inside the same Railway project, click **New** -> **GitHub Repo** and choose the same repository.
2. Go to the new service **Settings** -> **General** and change the service name to `guruai-frontend`.
3. Under **Settings** -> **Build**, set:
   * **Dockerfile Path**: `frontend.Dockerfile`
4. Go to the **Variables** tab and add:
   * `BACKEND_URL` = *[Your Backend Domain URL from Step 2, e.g., https://guruai-backend-production.up.railway.app]*
5. Go to **Settings** -> **Networking** and click **Generate Domain** to get the public URL for your Streamlit classroom Smart Board!

---

## ⚙️ Core Modules Breakdown

- **Guardrails (`guardrails.py`)**: Computes cosine similarity of queries against NCERT indexes. Queries with similarity scores $< 0.7$ are politely rejected with a student-friendly Hinglish response to maintain focus in the classroom.
- **Agents (`agents.py`)**: Uses NCERT context to compile explanations. Science queries focus on cause-and-effect and natural phenomena; Mathematics queries emphasize formulas and step-by-step derivations.
- **STT Handler (`stt_handler.py`)**: Utilizes local OpenAI Whisper (`base` model) to transcribe user speech audio bytes into query text.
- **TTS Handler (`tts_handler.py`)**: Synthesizes speech outputs using `edge-tts` with voice `hi-IN-SwaraNeural`. Automatically falls back to `gTTS` in offline/network-constrained environments.
- **Visuals (`visual_generator.py`)**: Draws dark-themed conceptual summary cards (`#1a2332` background, white/yellow text) using Matplotlib, returning a clean base64 image for the smart board.
