import os
import requests
import openai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

# Load environment variables from .env file
load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
MODEL_NAME = os.getenv("LLM_MODEL", "llama3.2:3b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VIDEO_ID = os.getenv("VIDEO_ID", "eHMIKOYcqSw")
OUTPUT_LANGUAGE = os.getenv("OUTPUT_LANGUAGE", "en")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

def fetch_transcript_text(video_id: str, languages=['fr', 'en']) -> str:
    """
    Fetch the transcript from a YouTube video and return the full concatenated text.
    Also saves the transcript in JSON format locally.
    """
    formatter = JSONFormatter()
    transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages)

    # save in JSON format
    json_text = formatter.format_transcript(transcript)
    with open("transcript.json", "w", encoding="utf-8") as f:
        f.write(json_text)

    print("Transcript saved to transcript.json")

    # contact text content
    return " ".join(snippet.text for snippet in transcript)

def summarize_with_llm(text: str) -> str:
    """
    Send the transcript to the selected LLM backend and return the summary.
    """
    prompt = f"Give me a resume in markdown format of this video transcription in {OUTPUT_LANGUAGE}:\n\n{text}"

    if LLM_BACKEND == "ollama":
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code != 200:
            raise RuntimeError(f"Ollama API call failed: {response.text}")
        return response.json()["response"]

    elif LLM_BACKEND == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")

def main():

    try:
        # recover transcription
        full_text = fetch_transcript_text(VIDEO_ID)

        # display text content
        print(f"\nTranscript:\n{full_text}")

        # send text content to the model to have a resume
        print(f"\nGenerating summary using {MODEL_NAME}...\n")
        summary = summarize_with_llm(full_text)
        print(f"📚 Summary:\n{summary}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()