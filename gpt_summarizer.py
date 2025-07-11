import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def summarize_transcript(transcript):
    """
    Summarize transcript and extract action items using GPT
    """
    try:
        # Create the prompt
        prompt = f"""
        Please analyze the following transcript and provide:
        1. A concise summary of the key points discussed
        2. A list of action items or next steps mentioned
        
        Transcript:
        {transcript}
        
        Please format your response as:
        
        SUMMARY:
        [Your summary here]
        
        ACTION ITEMS:
        - [Action item 1]
        - [Action item 2]
        - [etc.]
        """
        
        # Make API call using new OpenAI client
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as it's more cost-effective
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts and extracts action items."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        print(f"Raw GPT response: {repr(content)}")  # Debug line
        
        # Parse the response to separate summary and action items
        if content is None:
            lines = []
        else:
            lines = content.split('\n')
        summary = ""
        action_items = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            
            # Check for section headers
            if line.upper().startswith('SUMMARY:'):
                current_section = 'summary'
                # Check if summary content is on the same line
                summary_content = line.replace('SUMMARY:', '').strip()
                if summary_content:
                    summary = summary_content
            elif line.upper().startswith('ACTION ITEMS:'):
                current_section = 'action_items'
            elif current_section == 'summary' and line:
                # Add to summary (handle multi-line summaries)
                if summary:
                    summary += " " + line
                else:
                    summary = line
            elif current_section == 'action_items' and line:
                # Handle action items
                if line.startswith('- '):
                    action_items.append(line[2:].strip())
                elif line.startswith('• '):  # Handle bullet points
                    action_items.append(line[2:].strip())
                elif line and not line.upper().startswith(('SUMMARY:', 'ACTION ITEMS:')):
                    # Handle action items that don't start with - or •
                    action_items.append(line)
        
        # Clean up summary
        summary = summary.strip()
        
        # If parsing failed, provide fallback
        if not summary:
            summary = "Summary could not be parsed from the response."
        
        if not action_items:
            action_items = ["No specific action items identified."]
        
        print(f"Parsed summary: {repr(summary)}")  # Debug line
        print(f"Parsed action items: {action_items}")  # Debug line
        
        return summary, action_items
        
    except Exception as e:
        print(f"Error in summarize_transcript: {str(e)}")
        return f"Error generating summary: {str(e)}", ["Error extracting action items"]