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
    
def generate_ner(tokens, start_index):
    """
    Use the Google Gemini API to generate NER labels for a given list of tokens with token IDs.

    Args:
        tokens (list of str): A list of tokens to classify.
        start_index (int): The starting index of this chunk in the original email.

    Returns:
        list of str: A list of BIO tags corresponding to the tokens.
    """
    # Combine tokens into a numbered list
    numbered_tokens = [f"{start_index + i + 1}. {token}" for i, token in enumerate(tokens)]
    token_string = "\n".join(numbered_tokens)

    # Define the prompt
    prompt = f"""
    You are an intelligent assistant tasked with performing Named Entity Recognition (NER) to extract information
    about where, what, and when food is available from email content.

    ### Task:
    For each token, determine its BIO tag based on the provided entity types.

    ### Entity Types:
    - FOOD: Mentions of food or beverages (e.g., "Dinner," "Snacks," "Coffee").
    - FOOD-LOCATION: Locations where food is available (e.g., "Room 203," "Cafeteria").
    - FOOD-TIME: Dates or times when food is available (e.g., "December 28th at 7:30 PM").

    ### Response Format:
    Provide only the BIO tagging for each token in the format:
    Token_ID[space]Token[space]BIO-Tag

    NO explanations, NO extra text, and NO introductions. Just the BIO tagging, starting directly with:
    Token_ID[space]Token[space]BIO-Tag

    ### Input Tokens:
    {token_string}

    ### Response:
    """

    try:
        # Send the request to the Gemini API
        response = model.generate_content(prompt)
        response_text = response.text

        # Parse the response into BIO tags
        tokens_and_labels = response_text.strip().split("\n")
        labels = []

        for line in tokens_and_labels:
            parts = line.strip().split(" ")
            if len(parts) >= 3:  # Ensure valid Token ID, Token, BIO Tag format
                bio_tag = parts[-1]  # Take the last part as the BIO tag
                labels.append(bio_tag)
            else:
                print(f"Skipping invalid line: {line}")

        # Ensure token-label alignment
        if len(tokens) != len(labels):
            raise ValueError(f"Mismatch between tokens and labels in this chunk. Tokens: {len(tokens)}, Labels: {len(labels)}")

        return labels

    except Exception as e:
        print(f"Error during NER generation: {e}")
        raise e


