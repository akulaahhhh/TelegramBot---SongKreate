                #FOR DIRECT SNED TO PARTICULAR USER

# import requests

# TOKEN = "TELEGRAM-BOT-TOKEN"
# CHAT_ID = "USER-ID"
# AUDIO_PATH = "Song/blue (instrumental).mp3"
# THUMBNAIL_PATH = "Thumbnail/example.jpg"

# url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"

# files = {
#     "audio": open(AUDIO_PATH, "rb"),
#     "thumb": open(THUMBNAIL_PATH, "rb")  # Attach the thumbnail
# }
# data = {
#     "chat_id": CHAT_ID,
#     "title": "I am HIM",
#     "performer": "MR IDK"
# }

# response = requests.post(url, files=files, data=data)
# print(response.json())  # Check if the upload was successful


            #USING BOT
import os
import requests
import logging
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

# Ensure the timezone is set to pytz.utc
scheduler = AsyncIOScheduler(timezone=pytz.utc)
nest_asyncio.apply()

#Fetch .env file
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Store user data temporarily
user_data = {}

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    """Sends welcome instructions to the user."""
    await update.message.reply_text(
        "👋 Welcome to the SongKreate Bot!\n\n"
        "📌 How to use:\n"
        "1️⃣ Send me an audio file (MP3, M4A).\n"
        "2️⃣ Send me a thumbnail (JPG, 320x320 recommended).\n"
        "3️⃣ Send the song title and artist in this format:\n"
        "   *Title - Artist*\n"
        "4️⃣ I will send back your customized song! 🎶"
    )

async def handle_audio(update: Update, context: CallbackContext) -> None:
    """Handles incoming audio files."""
    audio = update.message.audio
    if not audio:
        await update.message.reply_text("❌ Please send a valid audio file!")
        return

    chat_id = update.message.chat_id
    user_data[chat_id] = {"audio": audio.file_id}

    await update.message.reply_text("✅ Audio received! Now, send me a thumbnail image 🖼️.")

async def handle_thumbnail(update: Update, context: CallbackContext) -> None:
    """Handles incoming image (thumbnail) files."""
    photo = update.message.photo
    if not photo:
        await update.message.reply_text("❌ Please send a valid image!")
        return

    chat_id = update.message.chat_id
    user_data[chat_id]["thumbnail"] = photo[-1].file_id  # Use the highest quality image

    await update.message.reply_text("✅ Thumbnail received! Now, send the song title and artist in this format:\n\n*Title - Artist*")

async def handle_text(update: Update, context: CallbackContext) -> None:
    """Handles text input (song title & artist)."""
    text = update.message.text
    if " - " not in text:
        await update.message.reply_text("❌ Please use the correct format: *Title - Artist*")
        return

    chat_id = update.message.chat_id
    title, artist = text.split(" - ", 1)

    user_data[chat_id]["title"] = title.strip()
    user_data[chat_id]["artist"] = artist.strip()

    # Confirm Details
    await update.message.reply_text(
        f"✅ Song: *{title.strip()}*\n"
        f"🎤 Artist: *{artist.strip()}*\n"
        f"📸 Thumbnail: ✅\n\n"
        f"🎵 Sending your customized song..."
    )

    # Send modified song
    await send_custom_song(update, context, chat_id)

async def send_custom_song(update: Update, context: CallbackContext, chat_id: int):
    """Sends the customized song with metadata and thumbnail using requests.post()."""
    
    bot_token = context.bot.token  # Get bot token
    api_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"

    # Retrieve stored data
    audio_file_id = user_data[chat_id]["audio"]
    title = user_data[chat_id]["title"]
    artist = user_data[chat_id]["artist"]
    thumbnail_file_id = user_data[chat_id]["thumbnail"]

    # Define local file paths
    audio_path = f"{chat_id}_song.mp3"
    thumbnail_path = f"{chat_id}_thumb.jpg"

    # ✅ Download audio
    audio_file = await context.bot.get_file(audio_file_id)
    await audio_file.download_to_drive(audio_path)

    # ✅ Download thumbnail
    thumb_file = await context.bot.get_file(thumbnail_file_id)
    await thumb_file.download_to_drive(thumbnail_path)

    # ✅ Send the request to Telegram API
    try:
        with open(audio_path, "rb") as audio, open(thumbnail_path, "rb") as thumb:
            files = {
                "audio": audio,
                "thumb": thumb  # 
            }
            data = {
                "chat_id": chat_id,
                "title": title,
                "performer": artist
            }
            response = requests.post(api_url, files=files, data=data)
            print(response.json())  # Debugging output

            if response.status_code != 200:
                await update.message.reply_text("❌ Error sending the song!")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

    # ✅ Cleanup
    os.remove(audio_path)
    os.remove(thumbnail_path)



    
async def main():
    """Starts the bot application."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.PHOTO, handle_thumbnail))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

