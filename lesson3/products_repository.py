from pymongo import MongoClient
from pymongo.database import Database


class ProductsRepository:
    __connection: MongoClient
    __db: Database

    def __init__(self):
        self.__connection = MongoClient()
        self.__db = self.__connection['products']

    def save_one_product(self, collection_name: str, product_info: dict):
        self.__db[collection_name].insert_one(product_info)

    def products_count(self, collection_name: str):
        return self.__db[collection_name].count_documents({})

    def find_products_by_total_score(self, collection_name: str, total_score):
        return self.__db[collection_name].find(
            {'total_score': {'$gt': total_score}}
        )

    def __del__(self):
        self.__connection.close()
        print(f'Закрыл соединение с БД {self.__db.name}')
