import whisper
import tempfile
import os

# Load Whisper model once when the file is imported
model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    # Save audio temporarily to disk
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    # Transcribe the file
    result = model.transcribe(temp_audio_path)

    # Delete the temp file after transcription
    os.remove(temp_audio_path)

    return result["text"]
