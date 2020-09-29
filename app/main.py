import random
import re
import uuid
import os
import mongodb

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from gtts import gTTS
from config import token, superusers, damdaw_chat_id, pepe_sticker_id, pepe_sticker_unique_id


def send_message_as_bot(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in superusers:
        context.bot.send_message(chat_id=damdaw_chat_id, text=update.message.text[9:])


def reply_with_sticker(update, context):
    update.message.reply_sticker(sticker=pepe_sticker_id)


def reply_with_text(update, context):
    if update.message.sticker.file_unique_id == pepe_sticker_unique_id:
        update.message.reply_text("Abriendo paraguas")


def message_with_buttons(update, context, text):
    keyboard = [
        [InlineKeyboardButton("Hilo Forocoches 🚗", url="https://www.forocoches.com/foro/showthread.php?t=8055773"),
         InlineKeyboardButton("Lista LinkedIn 👔", url="https://docs.google.com/spreadsheets/d/1E2CcYO5vP-cxC7X66hnVBvwykPBP7S52lFji_TM51Xk/edit#gid=0")],
        [InlineKeyboardButton("Enlace grupo 🔗", url="https://bit.ly/dawdam"),
         InlineKeyboardButton("¿Quién soy? 🐸", url="https://github.com/kazulu/el-paraguas-bot")],
        [InlineKeyboardButton("Recursos 🧑🏻‍💻", url="https://t.me/joinchat/AAAAAEuScA9YbrOnaeLLcg"),
         InlineKeyboardButton("Offtopic (+18) 😈", url="http://bit.ly/dawdamoff")],
    ]

    chat_id = update.effective_chat.id
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="Markdown")


def welcome_message(update, context):
    user_id = update.message.new_chat_members[0].id
    first_name = update.message.new_chat_members[0].first_name
    mention = "[" + first_name + "](tg://user?id=" + str(user_id) + ")"

    message_with_buttons(update, context, create_welcome_message(update, context, first_name, mention))


def create_welcome_message(update, context, first_name, username="novato"):
    sentences = []
    while len(sentences) < 3:
        random_sentence = random.choice(mongodb.get_welcome_sentences())
        if random_sentence not in sentences:
            sentences.append(random_sentence)
    message = ", ".join(sentences)
    replace = message.rfind(",")
    new_message = message[:replace] + " y" + message[replace + 1:]

    audio_final_message = f"Por la gloria {new_message}, yo te bendigo y te doy la bienvenida, {first_name}."
    tts = gTTS(text=audio_final_message, lang='es-es')
    filename = f"welcome_message_{uuid.uuid4().hex}.ogg"
    tts.save(filename)

    context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(filename, 'rb'))
    os.remove(filename)

    final_message = f"Por la gloria {new_message}, yo te bendigo y te doy la bienvenida, {username}."

    return final_message


def ban(update, context):
    update.message.reply_text("Venga tonto, pa tu casa")


def links(update, context):
    message_with_buttons(update, context, 'Aquí los tienes, vago de mierda.')


def pinned(update, context):
    message_with_buttons(update, context, 'Bienvenido al canal de DAW/DAM. Estos son los links diponibles actualmente:')


def add_welcome_message(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in superusers:
        mongodb.inser_new_sentence(update, update.message.text[5:])


def show_welcome_messages(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in superusers:
        message = '*🔥 Mensajes de bienvenida 🔥 *'
        i = 0
        for sentence in mongodb.get_welcome_sentences():
            i += 1
            message += f'\n \[{i}\] {sentence}'
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)


def remove_welcome_message(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in superusers:
        mongodb.remove_sentence(update, update.message.text[8:])


def main():
    # Inserts some welcomes sentences in the database in case there's none
    mongodb.insert_base_sentences()

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Custom Message Handler
    dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'abr(e|o|iendo) paraguas', re.IGNORECASE)), reply_with_sticker))
    dispatcher.add_handler(MessageHandler(Filters.sticker, reply_with_text))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))

    # Public commands
    dispatcher.add_handler(CommandHandler("ban", ban))
    dispatcher.add_handler(CommandHandler("links", links))
    dispatcher.add_handler(CommandHandler("pinned", pinned))

    # Welcome messages
    dispatcher.add_handler(CommandHandler("add", add_welcome_message))
    dispatcher.add_handler(CommandHandler("show", show_welcome_messages))
    dispatcher.add_handler(CommandHandler("remove", remove_welcome_message))
    dispatcher.add_handler(CommandHandler("message", send_message_as_bot))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
