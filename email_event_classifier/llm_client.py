import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the model
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_event_details_from_email(email_content):
    """
    Fetch event details from the provided email content using an LLM.

    Args:
        email_content (str): The email content to analyze.

    Returns:
        dict: Parsed response with event details.
    """
    prompt = f"""
    You are an intelligent assistant tasked with determining whether an email describes an event or gathering. An event or gathering is defined as a planned occasion where people come together, typically at a specific time and place.

    ### Task:
    1. Analyze the content of the email provided.
    2. Determine whether the email indicates an event or gathering.
    3. If it does indicate an event, provide the following details in a structured format:

    ### Response Format (JSON): {{
    "is_event": "Yes/No",
    "reason": "Brief explanation of why it is classified as an event or 'Not mentioned'",
    "time": "Extracted time in 'YYYY-MM-DD HH:MM' format or 'Not mentioned'",
    "location": "Extracted location or 'Not mentioned'",
    "food_mentioned": "Yes/No",
    "food_details": "Details about the food if mentioned, or 'Not mentioned'"
    }}
    
    ### Email to Analyze:
    {email_content}

    ### Response:
   """
    try:
        # Generate response from LLM
        response = model.generate_content(prompt)
        response_text = response.text
        cleaned_response = response_text.strip().strip('```json')

        # Parse response into a dictionary
        response_dict = json.loads(cleaned_response)
        return response_dict
    except json.JSONDecodeError:
        print("Error: LLM returned invalid JSON.")
        return {"error": "Invalid response from LLM"}
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        return {"error": str(e)}
