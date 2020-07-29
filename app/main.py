import random
import re
from config import token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

pepe_sticker_id = "CAACAgQAAxkBAAOyXw4dNEA3mbtu7tIXClE3_PGRKHkAAkEBAAKoISEGr2bGG23uS4saBA"
pepe_sticker_unique_id = "AgADQQEAAqghIQY"

welcome_sentences = (
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
    "del Espíritu Santo",
    "de la España programadora",
)


def reply_with_sticker(update, context):
    update.message.reply_sticker(sticker=pepe_sticker_id)


def reply_with_text(update, context):
    if update.message.sticker.file_unique_id == pepe_sticker_unique_id:
        update.message.reply_text("Abriendo paraguas")


def welcome_message(update, context):
    keyboard = [
        [InlineKeyboardButton("Hilo Forocoches 🚗", url="https://www.forocoches.com/foro/showthread.php?t=8055773"),
         InlineKeyboardButton("Lista LinkedIn 👔", url="https://docs.google.com/spreadsheets/d/1E2CcYO5vP-cxC7X66hnVBvwykPBP7S52lFji_TM51Xk/edit#gid=0")],
        [InlineKeyboardButton("Enlace grupo 🔗", url="https://bit.ly/dawdam"),
         InlineKeyboardButton("¿Quién soy? 🐸", url="https://github.com/kazulu/el-paraguas-bot")],
        [InlineKeyboardButton("Grupo de offtopic 😈", url="https://bit.ly/dawdam")],
    ]

    chat_id = update.effective_chat.id
    username = "@" + update.message.new_chat_members[0].username
    text = create_welcome_message(username)
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def create_welcome_message(username="novato"):
    sentences = []
    while len(sentences) < 3:
        random_sentence = random.choice(welcome_sentences)
        if random_sentence not in sentences:
            sentences.append(random_sentence)
    message = ", ".join(sentences)
    replace = message.rfind(",")
    new_message = message[:replace] + " y" + message[replace + 1:]

    return f"Por la gloria {new_message} yo te bendigo y te doy la bienvenida {username}."

def ban(update, context):
    update.message.reply_text("Venga tonto, pa tu casa")

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'abr(e|o|iendo) paraguas', re.IGNORECASE)), reply_with_sticker))
    dispatcher.add_handler(MessageHandler(Filters.sticker, reply_with_text))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))
    dispatcher.add_handler(CommandHandler("ban", ban))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
