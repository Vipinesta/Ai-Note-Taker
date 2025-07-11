from fastapi import FastAPI, UploadFile
from whisper_transcriber import transcribe_audio
from gpt_summarizer import summarize_transcript
from supabase_client import save_to_supabase
import traceback

app = FastAPI(title="AI Note Taker", version="1.0.0")

# Memory store for current transcript
transcript = ""

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile):
    global transcript
    try:
        audio_bytes = await file.read()
        text = transcribe_audio(audio_bytes)
        transcript += text + "\n"
        return {"transcribed_text": text}
    except Exception as e:
        print("⚠️ Error in /upload-audio:")
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/summarize/")
async def summarize():
    global transcript
    summary, action_items = summarize_transcript(transcript)
    save_to_supabase(transcript, summary, action_items)
    return {
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items
    }

@app.get("/")
async def root():
    return {"message": "AI Note Taker API is running!"}
