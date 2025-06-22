from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from main import fetch_transcript_text, summarize_with_llm, extract_video_id

app = FastAPI(title="YouTube Video Summarizer API")

# Serve the static HTML page
@app.get("/", response_class=FileResponse)
def serve_index():
    return "static/index.html"

# Serve any additional static files (JS, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request model for the API
class VideoRequest(BaseModel):
    video_ids: List[str]
    languages: List[str] = ["en"]
    translate: str = "en"

# REST endpoint to generate summary
@app.post("/summarize")
def summarize_video(request: VideoRequest):
    if not request.video_ids:
        return {"error": "No video ID provided."}
    
    results = {}

    video_ids = [extract_video_id(v) for v in request.video_ids]

    for video_id in video_ids:
        try:
            text = fetch_transcript_text(video_id, request.languages)
            summary = summarize_with_llm(text, request.translate)
            results[video_id] = {
                "transcript": text,
                "summary": summary
            }
        except Exception as e:
            results[video_id] = {"error": str(e)}

    return results