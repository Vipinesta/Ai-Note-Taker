import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables from .env file
load_dotenv()

# Get variables from .env - use the VARIABLE NAMES, not the values
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug: Check if variables are loaded (optional - remove after testing)
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {'*' * len(SUPABASE_KEY) if SUPABASE_KEY else 'None'}")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to save transcript + summary + action items
def save_to_supabase(transcript, summary, action_items):
    data = {
        "title": "Untitled Meeting",
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items
    }

    try:
        response = supabase.table("meetings").insert(data).execute()
        print("✅ Saved to Supabase")
    except Exception as e:
        print("❌ Failed to save to Supabase:", str(e))