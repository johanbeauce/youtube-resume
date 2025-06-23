import os
import argparse
import requests
import openai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from urllib.parse import urlparse, parse_qs

# Load environment variables from .env file
load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
MODEL_NAME = os.getenv("LLM_MODEL", "llama3.2:3b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")


def extract_video_ids(url_or_id: str) -> str:
    if "youtube.com" in url_or_id:
        parsed_url = urlparse(url_or_id)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [""])[0]
    return url_or_id

def fetch_transcript_text(video_id: str, languages: list[str]) -> str:
    video_transcription = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    return " ".join(snippet.text for snippet in video_transcription)

def summarize_with_llm(text: str, output_language: str) -> str:
    prompt = f"You are given a transcription of a YouTube video. Please provide: 1.	A concise summary in {output_language} (maximum 250 words). 2.	A structured report of the transcription in {output_language}, using markdown format (titles, bullet points, etc.). Make sure everything is written in {output_language} and clearly formatted. \"\"\"{text}\"\"\""

    if LLM_BACKEND == "ollama":
        return summarizeWithOllama(prompt)
    elif LLM_BACKEND == "openai":
        return summarizeWithOpenai(prompt)
    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")

def summarizeWithOpenai(prompt) :
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
        
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content.strip()

def summarizeWithOllama(prompt):
    response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
    if response.status_code != 200:
        raise RuntimeError(f"Ollama API call failed: {response.text}")
    return response.json()["response"]

def main():

    # CLI argument parsing
    args = parseCliArguments()
    video_ids = extract_video_ids(args.video_ids)

    for video_id in video_ids:
        try:
            print(f"\n🎬 Processing video: {video_id}")
            full_text = fetch_transcript_text(video_id, args.languages)

            print("\n📄 Transcript content:")
            print(full_text)

            print(f"\n🧠 Generating summary in {args.translate} using {MODEL_NAME} ({LLM_BACKEND})...")
            summary = summarize_with_llm(full_text, args.translate)
            print("\n📚 Summary:")
            print(summary)

        except Exception as e:
            print(f"❌ Error processing {video_id}: {e}")

def parseCliArguments():
    parser = argparse.ArgumentParser(description="Summarize one or more YouTube videos using a transcript and an LLM.")
    parser.add_argument("video_ids", nargs="+", help="One or more YouTube video IDs")
    parser.add_argument("--languages", nargs="+", default=["en"], help="Transcript language(s) to try (priority order)")
    parser.add_argument("--translate", default="en", help="Output language for the summary")
    return parser.parse_args()

if __name__ == "__main__":
    main()