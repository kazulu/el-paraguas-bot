import mongodb
from telegram import ParseMode

from config import superusers, damdaw_chat_id


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


def send_message_as_bot(update, context):
    user_id = update.message.from_user.name
    if update.effective_chat.type == 'private' and user_id in superusers:
        context.bot.send_message(chat_id=damdaw_chat_id, text=update.message.text[9:])