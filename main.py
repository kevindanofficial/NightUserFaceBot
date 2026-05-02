import telebot
import time
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Your Monero address
WALLET_ADDRESS = '86LJzL6HG5scAbQ2AKYVkQKUYteTPvoa63Tsup21vYp2fhfDWGE9PDzE3snwNUSVHFhNn6c7rCzv5iHJoSspBaMm2wU8gSy' 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Using HTML tags to make the address a one-tap copy block
    pitch_text = (
        "Hey! 😏 Want an exclusive face reveal?\n\n"
        "It costs $5 in XMR (Monero). Send it to my private wallet below:\n\n"
        f"<code>{WALLET_ADDRESS}</code>\n\n"
        "<i>(Tap the address above to copy it instantly)</i>\n\n"
        "Once you send it, just paste the <b>Transaction Hash (TXID)</b> here so I can verify!"
    )
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
            bot.send_message(message.chat.id, "[Error: 'masked_photo.jpg' is missing from the folder!]")
    else:
        bot.reply_to(message, "That's way too short to be a valid Monero Transaction Hash. Nice try! Paste the real 64-character hash after you pay.")

print("Troll bot is running locally in Termux...")
bot.polling()
