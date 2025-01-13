from email_event_classifier.llm_client import generate_ner
from email_event_classifier.bio_util import save_bio_to_file
import pandas as pd
from transformers import BertTokenizer
import time

# Load the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def process_email(email_content, bio_file, chunk_size=100):
    """
    Process a single email: tokenize, generate NER labels in chunks, and save in BIO format.

    Args:
        email_content (str): The content of the email.
        bio_file (str): The path to the BIO file where the output will be saved.
        chunk_size (int): The maximum number of tokens in each chunk.
    """
    # Tokenize the email content
    tokens = tokenizer.tokenize(email_content)

    # Split tokens into manageable chunks
    chunks = [(tokens[i:i + chunk_size], i) for i in range(0, len(tokens), chunk_size)]

    all_labels = []  # To collect labels for all chunks

    # Process each chunk independently
    for chunk, start_index in chunks:
        try:
            # Add time buffer to avoid rate limit
            time.sleep(6)

            # Generate labels for the chunk
            labels = generate_ner(chunk, start_index)
            all_labels.extend(labels)  # Combine results
        except Exception as e:
            print(f"Error during NER generation for chunk starting at {start_index}: {e}")
            return 

    # Check token-label alignment
    if len(tokens) != len(all_labels):
        print("Token-label length mismatch after processing all chunks. Skipping this email.")
        raise ValueError("Token-label length mismatch after processing all chunks.")

    # Save the tokens and labels in BIO format
    save_bio_to_file(tokens, all_labels, bio_file)
    print(f"Processed email saved to {bio_file}")

def process_all_emails(csv_file, bio_file):
    """
    Load emails from a CSV file, process them, and save results to a single BIO file.
    """
    # Load CSV data
    df = pd.read_csv(csv_file)

    # Only extract email where "is_event" is "Yes" and "food_mentioned" is "Yes"
    df = df[(df["is_event"] == "Yes") & (df["food_mentioned"] == "Yes")]

    # Get the email body content
    email_contents = df["body"].tolist()

    for i, email_content in enumerate(email_contents[125:150]):
        print(f"Processing email {i + 1}/{len(email_contents)}")
        process_email(email_content, bio_file)

if __name__ == "__main__":
    # File paths
    csv_file = "./resources/all_event_data.csv"
    bio_file = "./resources/all_event_data.bio"

    # Process all emails and save in a single BIO file
    process_all_emails(csv_file, bio_file)
