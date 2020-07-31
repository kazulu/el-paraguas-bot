import logging

from pymongo import MongoClient

from config import mongodb_database, mongodb_collection

welcome_sentences = [
    {'sentence': 'del Imperio que crea software'},
    {'sentence': 'de Jesucristo programador'},
    {'sentence': 'de Java'},
    {'sentence': 'de Python'},
    {'sentence': 'de Román el europeo'},
    {'sentence': 'de Moldavia'},
    {'sentence': 'de la ingeniera rusa'},
    {'sentence': 'de Cecilio'},
    {'sentence': 'de Ayuso'},
    {'sentence': 'de Leetcode'},
    {'sentence': 'del Clean Code'},
    {'sentence': 'de las apps basura del Play Store'},
    {'sentence': 'de España'},
    {'sentence': 'del Espíritu Santo'},
    {'sentence': 'de la España programadora'},
]


def insert_base_sentences():
    try:
        with MongoClient('localhost', 27017) as client:
            db = client[mongodb_database]
            collection = db[mongodb_collection]

            if collection.estimated_document_count() == 0:
                result = collection.insert_many(welcome_sentences)
                result.inserted_ids
    except:
        logging.error('Cannot connect to the server.')


def inser_new_sentence(update, sentence):
    try:
        with MongoClient('localhost', 27017) as client:
            db = client[mongodb_database]
            collection = db[mongodb_collection]

            collection.insert_one({'sentence': sentence})
            update.message.reply_text(f'"{sentence}" insertada. ✅')
    except:
        logging.error('Cannot connect to the server.')


def get_welcome_sentences():
    try:
        with MongoClient('localhost', 27017) as client:
            db = client[mongodb_database]
            collection = db[mongodb_collection]

            cursor = collection.find({})
            sentences = [x['sentence'] for x in cursor]
            return sentences
    except:
        logging.error('Cannot connect to the server.')


def remove_sentence(update, sentence):
    try:
        with MongoClient('localhost', 27017) as client:
            db = client[mongodb_database]
            collection = db[mongodb_collection]

            result = collection.delete_one({'sentence': sentence})
            if result.deleted_count == 1:
                update.message.reply_text(f'"{sentence}" eliminada. ✅')
            else:
                update.message.reply_text(f'"{sentence}" no pudo ser eliminada. ❌')
    except:
        logging.error('Cannot connect to the server.')
