# Assessli-Verse: The AI Voice Interviewer

This project is a submission for the Assessli AI Hackathon. It is a fully voice-driven interview simulator powered by a local AI model (Ollama + Llama 3) for conversation and a high-speed cloud API (Groq) for transcription.


## ✨ Key Features

-   **End-to-End Voice Conversation:** A complete, turn-by-turn voice interview experience.
-   **High-Performance Architecture:** Uses FastAPI for the backend and Streamlit for a responsive UI.
-   **Hybrid AI Model:** Leverages a local Llama 3 model (via Ollama) for free and private AI reasoning, while offloading speech-to-text to the ultra-fast Groq API for real-time performance.
-   **Local Text-to-Speech:** Uses `pyttsx3` to generate audio on the user's machine, ensuring privacy.
-   **Dynamic Performance Reports:** After the interview, a powerful agent analyzes the transcript to generate a structured report with a quantitative star rating and actionable feedback.


## 🛠️ Setup & Installation

### Prerequisites

-   Python 3.10+
-   A free **Groq API Key** for fast transcription.
-   **Ollama** installed and running for the local LLM.
-   **FFmpeg** installed on the system.

### Installation Steps

1.  **Install Ollama:**
    -   Download and install from [ollama.com](https://ollama.com/).
    -   In a separate terminal, run `ollama run llama3` to download the model and start the server. **Leave this terminal running.**

2.  **Install FFmpeg:**
    -   **Windows (Recommended):** Open PowerShell **as Administrator** and run `choco install ffmpeg`.
    -   **macOS (Recommended):** In Terminal, run `brew install ffmpeg`.

3.  **Clone this Repository:**
    ```bash
    git clone [your-repo-link]
    cd assessli-verse
    ```

4.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    ```

5.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Set Up Environment Variables:**
    -   Create a file named `.env` in the root of the project.
    -   Add your Groq API key to it:
        ```
        GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxx"
        ```

## 🚀 How to Run the Application

You will need **three separate terminals** running at the same time.

1.  **Terminal 1 (AI Server):**
    -   Make sure Ollama is running. If not, open a terminal and run:
        ```bash
        ollama run llama3
        ```

2.  **Terminal 2 (Backend Server):**
    -   Navigate to the project folder and activate the virtual environment.
    -   Run the robust command:
        ```bash
        python -m uvicorn backend:app
        ```

3.  **Terminal 3 (Frontend App):**
    -   Navigate to the project folder and activate the virtual environment.
    -   Run the Streamlit app:
        ```bash
        streamlit run app.py
        ```
    -   The application will open in your web browser.
