import os
import random
import uuid
import mongodb
from gtts import gTTS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import pepe_sticker_id, pepe_sticker_unique_id


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


def welcome_message(update, context):
    user_id = update.message.new_chat_members[0].id
    first_name = update.message.new_chat_members[0].first_name
    mention = "[" + first_name + "](tg://user?id=" + str(user_id) + ")"

    message_with_buttons(update, context, create_welcome_message(update, context, first_name, mention))