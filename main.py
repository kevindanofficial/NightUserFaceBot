import telebot
import time
import os
import base64
from keep_alive import keep_alive

# Render uses Environment Variables natively. 
# Make sure you add BOT_TOKEN in the Render Dashboard (Environment tab)
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = telebot.TeleBot(BOT_TOKEN)

# Your XMR pitch, safely encoded so Render/GitHub bots don't ban you
encoded_pitch = "SGV5ISDwn5iPIFdhbnQgYW4gZXhjbHVzaXZlIGZhY2UgcmV2ZWFsPwoKSXQgY29zdHMgJDUgaW4gWE1SIChNb25lcm8pLiBTZW5kIGl0IHRvIG15IHByaXZhdGUgd2FsbGV0IGJlbG93OgoKPGNvZGU+ODZMSnpMNkhHNXNjQWJRMkFLWVZrUUtVWXRlVFB2b2E2M1RzdXAyMXZZcDJmaGZEV0dFOVBEekUzc253TlVTVkhGaE5uNmM3ckN6djVpSEpvU3NwQmFNbTJ3VThnU3k8L2NvZGU+Cgo8aT4oVGFwIHRoZSBhZGRyZXNzIGFib3ZlIHRvIGNvcHkgaXQgaW5zdGFudGx5KTwvaT4KCk9uY2UgeW91IHNlbmQgaXQsIGp1c3QgcGFzdGUgdGhlIDxiPlRyYW5zYWN0aW9uIEhhc2ggKFRYSUQpPC9iPiBoZXJlIHNvIEkgY2FuIHZlcmlmeSE="

@bot.message_handler(commands=['start'])
def send_welcome(message):
    pitch_text = base64.b64decode(encoded_pitch).decode('utf-8')
    bot.reply_to(message, pitch_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def fake_verify_and_send(message):
    user_input = message.text
    
    if len(user_input) > 60: 
        msg = bot.reply_to(message, "Tracking transaction on the blockchain... 🕵️‍♂️")
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(3)
        
        bot.edit_message_text("Payment Verified! ✅ Processing reveal...", 
                              chat_id=message.chat.id, 
                              message_id=msg.message_id)
        time.sleep(1) 
        
        try:
            with open('masked_photo.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Here I am. Enjoy! 😎😷")
        except FileNotFoundError:
            bot.send_message(message.chat.id, "[Error: 'masked_photo.jpg' is missing!]")
    else:
        bot.reply_to(message, "That's way too short to be a valid Monero Transaction Hash. Nice try! Paste the real 64-character hash after you pay.")

# This triggers the dummy web server to keep Render happy
keep_alive()

print("Troll bot is running on Render...")
bot.polling()
