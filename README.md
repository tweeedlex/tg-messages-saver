# Telegram Messages Saver

This script saves Telegram messages, including media files, to a MongoDB database and uploads media files to Dropbox.

## Prerequisites

1. **Telegram API Credentials:**

   - Visit [Telegram Apps](https://my.telegram.org/auth) and log in with your Telegram account.
   - Create a new application to obtain the API ID and API Hash.
   - Use [@getmyid_bot](https://t.me/getmyid_bot) to get Chat ID. Forward a message from person to this bot to get it.

   ```dotenv
   TELEGRAM_API_ID=1111111
   TELEGRAM_API_HASH='012345678qwertyuiopasdfghjklzxcvbnm'
   TELEGRAM_CHAT_ID=1111111111
   ```

2. **MongoDB URI:**

   - Set up a MongoDB database on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a cluster, and obtain the connection URI with your credentials.

   ```dotenv
   MONGODB_URI="mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority"
   ```

3. **Dropbox Token:**

   - Create a new app on the [Dropbox App Console](https://www.dropbox.com/developers/apps).
   - Generate an access token for your app.
   - Make sure to write same foldername when creating app and in `.env` file

   ```dotenv
   DROPBOX_TOKEN='sl.qwertyuiopasdfghjklzxcvbnm'
   DROPBOX_FOLDER='/tg-messages-saver'
   ```

## Installation

1. Clone the repository or download ZIP-file

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and fill in the credentials obtained in the prerequisites section. You can use .env.example file for this

4. Run the script:

   ```bash
   python app.py
   ```

## Usage

- The script will listen for new messages in the specified Telegram chat and save them to MongoDB.
- Media files will be temporarily saved to a local folder, then uploaded to Dropbox.
