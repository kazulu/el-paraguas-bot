import re
import mongodb
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from config import token

from message_handlers import reply_with_sticker, reply_with_text, welcome_message
from private_commands import add_welcome_message, show_welcome_messages, remove_welcome_message, send_message_as_bot
from public_commands import ban, links, pinned


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

    # Private commands
    dispatcher.add_handler(CommandHandler("add", add_welcome_message))
    dispatcher.add_handler(CommandHandler("show", show_welcome_messages))
    dispatcher.add_handler(CommandHandler("remove", remove_welcome_message))
    dispatcher.add_handler(CommandHandler("message", send_message_as_bot))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
