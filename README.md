HEAD
# 🎙️ VBCUA — Voice-Based Concept Understanding Analyser

An AI-powered Streamlit web application that evaluates how well a user understands a technical concept by analyzing their **spoken explanation**. It combines speech-to-text, semantic similarity, speech fluency analysis, audio signal processing, AI scoring, and automatic PDF report generation.

---

## ✨ Features

- 🎤 **Speech-to-Text** — Transcription powered by OpenAI Whisper
- 🧠 **Semantic Similarity** — Sentence-BERT (`all-MiniLM-L6-v2`) compares your explanation to a reference answer
- 📊 **Speech Fluency Analysis** — Filler word detection, pause ratio, speech rate, vocal confidence
- 🔊 **Audio Signal Processing** — Waveform, RMS energy, zero-crossing rate, spectral features via Librosa
- 🎯 **AI Scoring Engine** — Weighted overall score (Concept 50% / Fluency 25% / Communication 25%) with letter grade
- 💡 **AI Feedback** — Strengths, weaknesses, improvement suggestions, and practice recommendations
- 📈 **Interactive Dashboard** — Circular score indicators, charts, gauges, and metric cards
- 📄 **PDF Report Generation** — Professional downloadable report with transcript, charts, and feedback

---

## 🛠️ Tech Stack

| Layer       | Technology                                  |
|-------------|----------------------------------------------|
| Frontend    | Streamlit                                    |
| Backend     | Python                                       |
| Speech-to-Text | OpenAI Whisper                            |
| Semantic Model | Sentence-BERT (`all-MiniLM-L6-v2`)        |
| Audio Processing | Librosa, SoundFile, NumPy               |
| Visualization | Matplotlib, Streamlit native charts       |
| PDF Reports | ReportLab                                    |
| NLP Utilities | NLTK, Transformers, Torch                  |

---

## 📁 Project Structure

```
VBCUA/
├── app.py                       # Main Streamlit entry point
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml              # Theme configuration
├── pages/
│   ├── home.py                  # Landing page
│   ├── analysis.py              # Upload + analysis trigger page
│   └── dashboard.py             # Results dashboard
├── components/
│   └── ui_components.py         # Reusable UI widgets (cards, badges, etc.)
├── models/
│   ├── speech_to_text.py        # Whisper transcription + filler word detection
│   ├── semantic_analysis.py     # Sentence-BERT similarity
│   └── audio_analysis.py        # Librosa-based signal processing
├── services/
│   ├── scoring.py                # AI scoring engine
│   ├── feedback.py               # AI feedback generator
│   ├── waveform.py               # Chart/waveform image generation
│   └── pdf_generator.py          # ReportLab PDF report builder
├── utils/
│   └── helpers.py                # Shared utilities + custom CSS
├── data/
│   ├── concepts.json             # 10 predefined concepts with reference answers
│   └── generate_sample_audio.py  # Synthetic sample audio generator
├── assets/
│   ├── audio/
│   │   └── sample_explanation.wav  # Sample audio for testing
│   └── images/
├── reports/                      # Generated PDF reports land here (optional)
└── tests/
    └── test_core.py              # Unit tests for scoring/fluency logic
```

---

## 🚀 Installation & Setup

### 1. Clone or extract the project
```bash
cd VBCUA
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Note on Whisper**: `openai-whisper` requires `ffmpeg` installed on your system.
> - macOS: `brew install ffmpeg`
> - Ubuntu/Debian: `sudo apt install ffmpeg`
> - Windows: download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### 4. (Optional) Generate the sample audio file
A sample is already included at `assets/audio/sample_explanation.wav`, but you can regenerate it:
```bash
python data/generate_sample_audio.py
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 📖 How to Use

1. **Home Page** — Read about the app and click "Start Analysis"
2. **Analysis Page**
   - Enter your name
   - Select a concept to explain (e.g., Machine Learning, Cloud Computing)
   - Upload a `.wav`, `.mp3`, or `.m4a` audio file of you explaining the concept
   - Click **"Run Full AI Analysis"**
3. **Dashboard**
   - View your overall score, grade, and sub-scores
   - Explore tabs: Transcript, Concept Understanding, Fluency Analysis, AI Feedback
   - Generate and download your PDF report

---

## ⚙️ Evaluation Logic

```
Overall Score = (Semantic Similarity × 50%)
              + (Speech Fluency × 25%)
              + (Communication Quality × 25%)
```

| Score Range | Grade |
|-------------|-------|
| 90–100      | A+    |
| 80–89       | A     |
| 70–79       | B     |
| 60–69       | C     |
| < 60        | D     |

| Similarity | Understanding Level |
|------------|----------------------|
| ≥ 75%      | Excellent            |
| 55–74%     | Good                 |
| 35–54%     | Average              |
| < 35%      | Poor                 |

---

## 🧩 Extending the App

- **Add new concepts**: edit `data/concepts.json` — add a `reference` explanation and `key_concepts` list
- **Swap models**: change the Whisper model size in `models/speech_to_text.py` (`tiny`/`base`/`small`/`medium`/`large`) or the SBERT model in `models/semantic_analysis.py`
- **Add live recording**: integrate `streamlit-audiorecorder` or `streamlit-mic-recorder` in `pages/analysis.py`
- **Custom scoring weights**: adjust weights in `services/scoring.py`

---

## 📝 Notes

- If `openai-whisper`, `sentence-transformers`, or `librosa` are not installed, the app gracefully falls back to demo/heuristic modes so the UI remains fully functional for testing.
- First run will download the Whisper and SBERT models (a few hundred MB) — ensure you have an internet connection and sufficient disk space.

---

## 📄 License

This project is provided as an academic/portfolio deliverable. Free to use and modify.
=======
# Voice-Based-Concept-Understanding-Analyser
AI-powered web application that evaluates students' conceptual understanding through speech analysis and semantic similarity.
>>>>>>> a4ed48ff69cf843b6d95df748c7ba30bc7c8f2f6
