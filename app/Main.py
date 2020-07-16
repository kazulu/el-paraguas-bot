import re, random
from telegram.ext import Updater, MessageHandler, Filters
from app.config import token

pepe_sticker_id = "CAACAgQAAxkBAAOyXw4dNEA3mbtu7tIXClE3_PGRKHkAAkEBAAKoISEGr2bGG23uS4saBA"
pepe_sticker_unique_id = "AgADQQEAAqghIQY"

welcome_sentences = [
    "del Imperio que crea software",
    "de Jesucristo programador",
    "de Java",
    "de Python",
    "de Román el europeo",
    "de Moldavia",
    "de la ingeniera rusa",
    "de Cecilio",
    "de Ayuso",
    "de Leetcode",
    "del Clean Code",
    "de las apps basura del Play Store",
    "de España",
    "del Espíritu Santo"
]

def reply_with_sticker(update, context):
    update.message.reply_sticker(sticker = pepe_sticker_id)

def reply_with_text(update, context):
    if update.message.sticker.file_unique_id == pepe_sticker_unique_id:
        update.message.reply_text("Abriendo paraguas")

def welcome_message(update, context):
    update.message.reply_text(create_welcome_message())

def create_welcome_message():
    sentences = []
    while len(sentences) < 3:
        random_sentence = random.choice(welcome_sentences)
        if random_sentence not in sentences:
            sentences.append(random_sentence)
    message = ", ".join(sentences)
    replace = message.rfind(",")
    new_message = message[:replace] + " y" + message[replace + 1:]

    return "Por la gloria " + new_message + " yo te bendigo y te doy la bienvenida."

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'abr(e|o|iendo) paraguas', re.IGNORECASE)), reply_with_sticker))
    dispatcher.add_handler(MessageHandler(Filters.sticker, reply_with_text))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()