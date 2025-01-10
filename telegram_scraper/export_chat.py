import os
import csv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start the client
    await client.start(phone=phone_number)
    print("Client Created")

    # Ensure the user is authorized
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            code = input('Enter the code you received: ')
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input('Two-step verification enabled. Please enter your password: ')
            await client.sign_in(password=password)

    # Retrieve the list of dialogs (conversations)
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))

    # Filter the chats to find the one with the specified name
    chat_name = input('Enter the chat name to export: ')
    target_chat = None
    for chat in result.chats:
        if chat.title == chat_name:
            target_chat = chat
            break

    if target_chat is None:
        print(f'Chat "{chat_name}" not found.')
        return

    print(f'Found chat: {target_chat.title}')

    # Create a directory for the chat export
    export_dir = f'export_{target_chat.title}'
    os.makedirs(export_dir, exist_ok=True)

    # Open a CSV file to write the chat history
    with open(os.path.join(export_dir, f'{target_chat.title}.csv'), 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Sender', 'Message', 'Date'])

        # Iterate over the messages in the chat
        async for message in client.iter_messages(target_chat):
            sender = await message.get_sender()
            if sender:  # Check if sender is not None
                sender_name = (
                    sender.username if sender.username
                    else f'{sender.first_name or ""} {sender.last_name or ""}'.strip()
                )
            else:
                sender_name = 'Unknown Sender'
            writer.writerow([sender_name, message.message, message.date.strftime('%Y-%m-%d %H:%M:%S')])

    print(f'Chat history exported to {export_dir}/{target_chat.title}.csv')

# Run the main function within the client context
with client:
    client.loop.run_until_complete(main())
