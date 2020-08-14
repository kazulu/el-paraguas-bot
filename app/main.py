import random
import re
import schedule
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async

import mongodb
from config import token, welcome_users

pepe_sticker_id = "CAACAgQAAxkBAAOyXw4dNEA3mbtu7tIXClE3_PGRKHkAAkEBAAKoISEGr2bGG23uS4saBA"
pepe_sticker_unique_id = "AgADQQEAAqghIQY"

pole = True


def reply_with_sticker(update, context):
    update.message.reply_sticker(sticker=pepe_sticker_id)
    is_la_pole(update, context)


def reply_with_text(update, context):
    if update.message.sticker.file_unique_id == pepe_sticker_unique_id:
        update.message.reply_text("Abriendo paraguas")
    is_la_pole(update, context)


def message_with_buttons(update, context, text):
    keyboard = [
        [InlineKeyboardButton("Hilo Forocoches 🚗", url="https://www.forocoches.com/foro/showthread.php?t=8055773"),
         InlineKeyboardButton("Lista LinkedIn 👔", url="https://docs.google.com/spreadsheets/d/1E2CcYO5vP-cxC7X66hnVBvwykPBP7S52lFji_TM51Xk/edit#gid=0")],
        [InlineKeyboardButton("Enlace grupo 🔗", url="https://bit.ly/dawdam"),
         InlineKeyboardButton("¿Quién soy? 🐸", url="https://github.com/kazulu/el-paraguas-bot")],
        [InlineKeyboardButton("Grupo de offtopic (+18) 😈", url="http://bit.ly/dawdamoff")],
    ]

    chat_id = update.effective_chat.id
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="Markdown")


def welcome_message(update, context):
    user_id = update.message.new_chat_members[0].id
    first_name = update.message.new_chat_members[0].first_name
    mention = "[" + first_name + "](tg://user?id=" + str(user_id) + ")"

    message_with_buttons(update, context, create_welcome_message(mention))


def create_welcome_message(username="novato"):
    sentences = []
    while len(sentences) < 3:
        random_sentence = random.choice(mongodb.get_welcome_sentences())
        if random_sentence not in sentences:
            sentences.append(random_sentence)
    message = ", ".join(sentences)
    replace = message.rfind(",")
    new_message = message[:replace] + " y" + message[replace + 1:]

    return f"Por la gloria {new_message} yo te bendigo y te doy la bienvenida {username}."


def ban(update, context):
    update.message.reply_text("Venga tonto, pa tu casa")


def links(update, context):
    message_with_buttons(update, context, 'Aquí los tienes vago de mierda.')


def add_welcome_message(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in welcome_users:
        mongodb.inser_new_sentence(update, update.message.text[5:])


def show_welcome_messages(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in welcome_users:
        message = '*🔥 Mensajes de bienvenida 🔥 *'
        i = 0
        for sentence in mongodb.get_welcome_sentences():
            i += 1
            message += f'\n \[{i}\] {sentence}'
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)


def remove_welcome_message(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in welcome_users:
        mongodb.remove_sentence(update, update.message.text[8:])


def reset_pole():
    global pole
    pole = False


@run_async
def schedule_everyday():
    while True:
        schedule.run_pending()
        time.sleep(1)


def is_la_pole(update, context):
    global pole
    if not pole:
        update.message.reply_text('Has hecho la pole, felicidades. 💈')
        pole = True


def main():
    # Inserts some welcomes sentences in the database in case there's none
    mongodb.insert_base_sentences()

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Resets la pole every day
    schedule.every().day.at("00:00").do(reset_pole)
    schedule_everyday()

    # Custom Message Handler
    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'abr(e|o|iendo) paraguas', re.IGNORECASE)), reply_with_sticker))
    dispatcher.add_handler(MessageHandler(Filters.sticker, reply_with_text))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))

    # Public commands
    dispatcher.add_handler(CommandHandler("ban", ban))
    dispatcher.add_handler(CommandHandler("links", links))

    # Welcome messages
    dispatcher.add_handler(CommandHandler("add", add_welcome_message))
    dispatcher.add_handler(CommandHandler("show", show_welcome_messages))
    dispatcher.add_handler(CommandHandler("remove", remove_welcome_message))

    # Pole
    dispatcher.add_handler(MessageHandler(Filters.all, is_la_pole))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
