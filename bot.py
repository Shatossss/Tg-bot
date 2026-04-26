import telebot
import os
from flask import Flask
from threading import Thread

TOKEN = "8620930680:AAGMFBld3aXdu77gy32TO4S-fHt_rE_Zn58"
ADMIN_ID = 7853632822

bot = telebot.TeleBot(TOKEN)
app = Flask("app")

@app.route("/")
def home():
    return "Бот 24/7 активний"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Напиши свою плітку.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id != ADMIN_ID:
        user = message.from_user
        username = f"@{user.username}" if user.username else "немає"
        info = f"📩 НОВА ПЛІТКА!\n\n👤 Від: {user.first_name}\n🔗 Юзер: {username}\n🆔 ID: {user.id}\n\n💬 Текст: {message.text}"
        try:
            bot.send_message(ADMIN_ID, info)
            bot.send_message(message.chat.id, "Плітка надіслана")
        except:
            pass

# Запуск сервера та бота
Thread(target=run_server).start()
bot.infinity_polling()
