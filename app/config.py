import os

token = os.getenv("TELEGRAM_TOKEN")

# MongoDB
mongodb_database = 'paraguasBot'
mongodb_collection = 'welcomeSentences'
mongodb_host = 'mongo'
mongodb_port = 27017

# Users who can add welcome sentences
superusers = ['@natan', '@kazulu']

# about
damdaw_chat_id = -1001155539490

# stickers
pepe_sticker_id = "CAACAgQAAxkBAAOyXw4dNEA3mbtu7tIXClE3_PGRKHkAAkEBAAKoISEGr2bGG23uS4saBA"
pepe_sticker_unique_id = "AgADQQEAAqghIQY"