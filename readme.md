# YouTube Video Summarizer

**YouTube Video Summarizer** is a tool that generates a text summary of any public YouTube video using its video ID.

## 🎯 Purpose

The goal of this project is to make video content more accessible and skimmable.

Whether you're short on time or simply prefer reading over watching, this tool allows you to:
- Get a quick overview of a video's content before watching it
- Rely entirely on the summary if you don't enjoy consuming content in video format
- Save time when researching topics by extracting key points from long videos

It fetches the video's transcript and uses a configurable Large Language Model (LLM) such as Llama 3 (locally via Ollama) or OpenAI's ChatGPT to generate a concise and readable summary.

## 🚀 Features

- 🔍 Fetch the transcript from a YouTube video
- 🧠 Generate summaries using:
  - A local model via [Ollama](https://ollama.com/)
  - OpenAI's GPT models (e.g. `gpt-3.5-turbo`, `gpt-4`) using an API key
- ⚙️ Fully configurable through a `.env` file
- 💾 Saves raw transcript as JSON

## 🛠 Requirements

- Python 3.9+
- [Poetry](https://python-poetry.org/)
- Internet connection (for transcript fetching or OpenAI)
- If using Ollama:
  - [Install Ollama](https://ollama.com/download) and pull the desired model, e.g. `ollama pull llama3`

## 📦 Installation

```bash
git clone https://github.com/johanbeauce/youtube-resume.git
cd youtube-resume
poetry install
```

Then install additional dependencies:

```bash
poetry add youtube-transcript-api requests python-dotenv
# If you plan to use OpenAI:
poetry add openai
```

## ⚙️ Configuration

Create a .env file at the root of the project with the following structure:

```text
# Choose LLM backend: 'ollama' or 'openai'
LLM_BACKEND=ollama

# Model name for each backend
LLM_MODEL=llama3.2:3b         # For Ollama
# LLM_MODEL=gpt-3.5-turbo     # For OpenAI

# Required if using OpenAI
OPENAI_API_KEY=sk-your-api-key

# Optional: Customize Ollama endpoint
OLLAMA_URL=http://localhost:11434/api/generate
```

⚠️ Do not include comments after values in your .env file (unlike Bash, they are not ignored).

## 🧪 Usage

### Via CLI
You can pass one or more YouTube video IDs and configure transcript and summary languages via CLI:

```bash
poetry run python main.py <video_id_1> <video_id_2> ... --languages <transcript_lang_1> <transcript_lang_2> --translate <summary_lang>
```

### Via Web Page
You can use the **web interface** to summarize one or more YouTube videos.

Simply run the backend server:

```bash
poetry run uvicorn api:app --reload
```

Then open your browser at:

📍 http://localhost:8000

The interface allows you to:
- Paste a YouTube video ID or full URL
- Choose transcript language(s) (e.g. fr, en)
- Select output language for the summary (e.g. fr, en)
- View the summary rendered in markdown format
- See a spinner while the model is working

### 🔧 Examples
```bash
# One video, transcript in French preferred, summary in French
poetry run python main.py eHMIKOYcqSw --languages fr en --translate fr

# Multiple videos, default transcript language is English, summary in English
poetry run python main.py abc123 def456 --languages en --translate en
```

- --languages accepts one or more language codes (in order of priority) for transcript selection.
- --translate specifies the desired output language for the summary.
- The transcript will be saved as <video_id>_transcript.json in the project folder.


## 📚 Output Example

### Via CLI
```text
🎬 Processing video: eHMIKOYcqSw
✅ Transcript for eHMIKOYcqSw saved to eHMIKOYcqSw_transcript.json

📄 Transcript content:
Bonjour à tous, aujourd'hui on va parler d'algorithmes et de structures de données...

🧠 Generating summary in fr using llama3.2:3b (ollama)...

📚 Summary:
- Cette vidéo explique les concepts fondamentaux des algorithmes en utilisant des exemples concrets.
- Elle aborde les structures comme les piles, files, listes chaînées, et leur utilité dans la résolution de problèmes.
```

### Via Web Page

Once a video is processed, the summary will be rendered in a clean markdown format like:

```markdown
## Key Concepts Covered

- This video explains fundamental algorithm design principles.
- Topics include data structures like stacks, queues, and linked lists.
- The summary is generated using a local or cloud-based LLM.
```

## 🧼 Project Structure

```text
.
├── main.py
├── .env
├── pyproject.toml
└── README.md
```

## 📄 License

MIT License