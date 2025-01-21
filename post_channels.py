import telebot#YEPAKI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bT = 'ABCD:12345';bot = telebot.TeleBot(bT)
chs = ['@user1', '@user2']#[Channels up to 35channel (Public only)]
last_message_ids = {} #YEPAKI
@bot.message_handler(commands=['go'])
def start_message(message):
    bot.reply_to(message,"— Hi sir, I'm a bot to help you manage your channels.",reply_markup=main_menu())
def main_menu():#YEPAKI
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("• New Post.", callback_data="post_message"),InlineKeyboardButton("• Pin LastMessages.", callback_data="pin_last_messages"))
    return markup#Here Buttons(Inline)
def post_new_message(chat_id):
    msg = bot.send_message(chat_id, "• Send the message or photo you want to post in all channels:")
    bot.register_next_step_handler(msg, publish_message)#YEPAKI
def publish_message(message):
    global last_message_ids
    last_message_ids = {}#[Saving messages to delete them.]
    try:#YEPAKI
        if message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)#YEPAKI
            downloaded_file = bot.download_file(file_info.file_path)
            with open("P.jpg", "wb") as photo_file:
                photo_file.write(downloaded_file)
            
            with open("P.jpg", "rb") as photo:
                for channel in chs:#YEPAKI
                    sent_msg = bot.send_photo(channel, photo, caption=message.caption or "")#In the last 3 lines there is error, bot send photo to 1 channel as Max.
                    last_message_ids[channel] = sent_msg.message_id
        else:
            for channel in chs:#YEPAKI
                sent_msg = bot.send_message(channel, message.text)
                last_message_ids[channel] = sent_msg.message_id        
        bot.reply_to(message, "• Posted in all channels ✅.")#YEPAKI
    except Exception as e:
        bot.reply_to(message, f"• Error: {e}❎")
def pin_last_messages(chat_id):
    global last_message_ids
    if last_message_ids:
        for channel, message_id in last_message_ids.items():
            try:#YEPAKI
                bot.pin_chat_message(channel, message_id)
            except Exception as e:
                bot.send_message(chat_id, f"• Error pinning in {channel}: {e}")
        bot.send_message(chat_id, "• Pinned all last messages ✅.")
    else:
        bot.send_message(chat_id, "• No messages to pin.")#YEPAKI

# [Buttons Services]
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "post_message":
        post_new_message(call.message.chat.id)
    elif call.data == "pin_last_messages":
        pin_last_messages(call.message.chat.id)

# [RunBot]
print("Started.")
bot.infinity_polling()