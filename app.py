import os
import random
import string
from telethon.sync import TelegramClient, events
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dropbox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram configurations
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))

# MongoDB configuration
uri = os.getenv('MONGODB_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["messages"]

# Dropbox configuration
dropbox_token = os.getenv('DROPBOX_TOKEN')
dropbox_folder = os.getenv('DROPBOX_FOLDER')

# Initialize Dropbox client
dbx = dropbox.Dropbox(dropbox_token)

print("App started, press Ctrl + C to quit")

# Ensure the 'media' folder exists
media_folder = 'temp'
os.makedirs(media_folder, exist_ok=True)

def sanitize_filename(filename):
    # Replace colons with underscores
    return filename.replace(':', '_')

with TelegramClient('name', api_id, api_hash) as client:
    # @client.on(events.NewMessage())
    @client.on(events.NewMessage(chats=chat_id)) # only messages from chat with chat_id will be handled
    async def message_handler(event):
        # check if message is from correct user
        if (chat_id != event.message.sender_id):
            return
        print(event.message)
        # save message to db
        db.messages.insert_one({"message": event.message.message, "user_id": event.message.sender_id, "date": event.message.date})

        if event.message.media:
            media_type = event.message.media.__class__.__name__
            file_extension = event.message.file.ext if hasattr(event.message.file, 'ext') else 'unknown'

            # create 4 random symbols for filename
            random_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) 
            # temporarly save file to local folder
            media_filename = f"{random_hash}_{sanitize_filename(str(event.message.date))}_{event.message.sender_id}.{file_extension}"
            media_path = os.path.join(media_folder, media_filename)
            db.media.insert_one({"filename": media_filename, "user_id": event.message.sender_id, "date": event.message.date})
            await event.message.download_media(file=media_path)
            print(f"Saved {media_type} to {media_path}")

            # upload file to Dropbox
            with open(media_path, 'rb') as file:
                dropbox_path = f"{dropbox_folder}/{media_filename}"
                dbx.files_upload(file.read(), dropbox_path)
                print(f"Uploaded {media_type} to Dropbox: {dropbox_path}")

            # remove file from local folder
            os.remove(media_path)

    client.run_until_disconnected()
