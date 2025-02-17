
# 🎵 SongKreate - A Telegram Custom Song Bot

A **Telegram bot** that allows users to send an audio file, provide a thumbnail, and set the song title and artist name. The bot then returns the customized audio file with metadata and an embedded thumbnail. 🚀

---

## 📌 Features
✅ Receive and process audio files (MP3, M4A)  
✅ Accept custom thumbnails (JPG, PNG)  
✅ Set song **title** and **artist**  
✅ Send back the modified audio file with metadata and thumbnail  
✅ Easy deployment using **Railway**  

---

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/akulaahhhh/TelegramBot---SongKreate.git
cd TelegramBot---SongKreate
```

### **2️⃣ Install Dependencies**
Ensure you have **Python 3.10+** installed.

```sh
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
Copy the `.env.example` file and rename it to `.env`:

```sh
cp .env.example .env
```

Then, open `.env` and fill in your **Telegram Bot Token**:

```env
TOKEN=your_telegram_bot_token
```

---

## 🚀 Running the Bot

### **Locally**
Run the bot using:
```sh
python bot.py
```

### **Deploying to Railway**
1. Push your project to **GitHub**.
2. Create a new Railway project.
3. Connect your repository.
4. Add environment variables in Railway’s dashboard (copy from your `.env`).
5. Deploy! 🎉

---

## 📜 Usage Guide
1️⃣ **Send an audio file** (MP3 or M4A).  
2️⃣ **Send a thumbnail image** (JPG, 320x320 recommended).  
3️⃣ **Send the song title and artist** in this format:  
   ```
   Title - Artist
   ```
4️⃣ The bot will send back your customized song! 🎶

---

## 🛠️ Technologies Used
- **Python**
- **python-telegram-bot v20+**
- **AsyncIO**
- **APScheduler**
- **Railway for Deployment**

---

## 🤝 Contributing
Feel free to fork this repository, submit issues, or create pull requests!

---

## 📄 License
This project is licensed under the MIT License.

---

### 🌟 Show Some Love!
If you like this project, consider giving it a ⭐ on **GitHub**! ❤️

