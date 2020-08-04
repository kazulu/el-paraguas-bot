import os

token = os.getenv("TELEGRAM_TOKEN")

# MongoDB
mongodb_database = 'paraguasBot'
mongodb_collection = 'welcomeSentences'
mongodb_host = 'mongo'
mongodb_port = 27017

# Users who can add welcome sentences
welcome_users = ['@natan', '@kazulu']