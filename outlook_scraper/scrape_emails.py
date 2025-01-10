import os
import win32com.client
from datetime import datetime
import argparse
import csv

def scrape_emails(start_date=None, end_date=None):
    print("Starting email scraping...")

    # Initialize the Outlook application
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # Access the inbox folder (6 represents the inbox)
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items

    # Apply date filters if specified
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        # Set to a very early date if not specified
        start_date = datetime(1970, 1, 1)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        # Set to the current date and time if not specified
        end_date = datetime.now()

    # Format dates to match Outlook's expected format: "DD/MM/YYYY HH:MM AM/PM"
    start_date_str = start_date.strftime("%d/%m/%Y %I:%M %p")
    end_date_str = end_date.strftime("%d/%m/%Y %I:%M %p")

    # Create a restriction string for the date range
    restriction = f"[ReceivedTime] >= '{start_date_str}' AND [ReceivedTime] <= '{end_date_str}'"
    print(f"Restriction string: {restriction}")  # Debug print to ensure correctness
    messages = messages.Restrict(restriction)

    # return messages 
    return messages

    # for message in messages:
    #     try:
    #         sender = message.SenderEmailAddress
    #         subject = message.Subject
    #         received_time = message.ReceivedTime
    #         body = message.Body

    #         print(f"From: {sender}")
    #         print(f"Subject: {subject}")
    #         print(f"Received: {received_time}")
    #         print(f"Body Preview: {body[:100]}...")  # Print the first 100 characters of the body
    #         print("-" * 50)

    #     except Exception as e:
    #         print(f"Error processing message: {e}")

# Example usage
# scrape_emails(start_date="2024-12-01", end_date="2024-12-31")

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Scrape emails and save to CSV.")
    parser.add_argument("--start_date", type=str, help="Start date in YYYY-MM-DD format", required=False)
    parser.add_argument("--end_date", type=str, help="End date in YYYY-MM-DD format", required=False)
    parser.add_argument("--output_file", type=str, help="Output CSV file path", default="emails.csv")
    args = parser.parse_args()

    # Call scrape_emails method to fetch emails
    messages = scrape_emails(start_date=args.start_date, end_date=args.end_date)

    # Save emails to a CSV file
    print("Saving emails to CSV...")
    with open(args.output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Content', 'Is_Event'])  # CSV headers: Content and Is_Event (blank for manual labeling)

        for message in messages:
            try:
                body = message.Body.strip() if message.Body else "No Content"
                writer.writerow([body, ""])  # Leave the 'Is_Event' column blank for manual labeling
            except Exception as e:
                print(f"Error processing message: {e}")

    print(f"Emails saved to {args.output_file}")