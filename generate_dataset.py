from outlook_scraper.scrape_emails import scrape_emails
from email_event_classifier.llm_client import get_event_details_from_email
from email_event_classifier.csv_util import write_to_csv
import time

def generate_dataset(start_date=None, end_date=None):
    # Get messages within the specified date range from Outlook
    messages = scrape_emails(start_date, end_date)

    # For each message
    for message in messages:
        # Extract the email in dict format
        try:
            email_content = {
                "sender": message.SenderEmailAddress,
                "received_time": message.ReceivedTime,
                "subject": message.Subject,
                "body": message.Body
            }
        except Exception as e:
            print(f"Error processing email: {e}")
            continue
        
        # buffer 10 seconds to compensate for google api rate limit
        time.sleep(6)

        try: 
            # Get event details from the email content
            event_details = get_event_details_from_email(email_content)
        except Exception as e:
            print(f"Error getting event detail: {e}")
            continue

        merged_data = email_content | event_details

        # Write the event details to a CSV file
        write_to_csv(merged_data, ".\\resources\\event_dataset4.csv", list(merged_data.keys()))

if __name__ == "__main__":
    # generate_dataset(start_date="2024-06-15", end_date="2024-08-15")
    # generate_dataset(start_date="2024-04-15", end_date="2024-06-14")
    # generate_dataset(start_date="2024-02-15", end_date="2024-04-14")    
    generate_dataset(start_date="2023-12-15", end_date="2024-02-14")
    # generate_dataset(start_date="2023-10-15", end_date="2023-12-14")
    # generate_dataset(start_date="2023-08-15", end_date="2023-10-14")
    # generate_dataset(start_date="2023-06-15", end_date="2023-08-14")

