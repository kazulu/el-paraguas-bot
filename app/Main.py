import re
from telegram.ext import Updater, MessageHandler, Filters
from app.config import token

pepe_sticker_id = "CAACAgQAAxkBAAOyXw4dNEA3mbtu7tIXClE3_PGRKHkAAkEBAAKoISEGr2bGG23uS4saBA"
pepe_sticker_unique_id = "AgADQQEAAqghIQY"

def reply_with_sticker(update, context):
    update.message.reply_sticker(sticker = pepe_sticker_id)

def reply_with_text(update, context):
    if update.message.sticker.file_unique_id == pepe_sticker_unique_id:
        update.message.reply_text("Abriendo paraguas")

def welcome_message(update, context):
    update.message.reply_text("Por la gloria del Imperio, bienvenido")

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'paraguas', re.IGNORECASE)), reply_with_sticker))
    dispatcher.add_handler(MessageHandler(Filters.sticker, reply_with_text))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()