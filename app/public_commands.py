from message_handlers import message_with_buttons


def ban(update, context):
    update.message.reply_text("Venga tonto, pa tu casa")


def links(update, context):
    message_with_buttons(update, context, 'Aquí los tienes, vago de mierda.')


def pinned(update, context):
    message_with_buttons(update, context, 'Bienvenido al canal de DAW/DAM. Estos son los links diponibles actualmente:')