from pymongo import MongoClient
from pymongo.database import Database


class NewsRepository:
    __connection: MongoClient
    __db: Database
    __collection_name = 'news'

    def __init__(self):
        self.__connection = MongoClient()
        self.__db = self.__connection['news']

    def save_one_news(self, news_info: dict):
        self.__db[self.__collection_name].update_one({'_id': news_info['_id']}, {'$set': news_info}, upsert=True)

    def insert_one(self, news_info: dict):
        self.__db[self.__collection_name].insert_one(news_info)

    def find_all(self):
        return self.__db[self.__collection_name].find({})

    def news_count(self):
        return self.__db[self.__collection_name].count_documents({})

    def __del__(self):
        self.__connection.close()
        print(f'Закрыл соединение с БД {self.__db.name}')
