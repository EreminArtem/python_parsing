from pymongo import MongoClient
from pymongo.database import Database


class ProfessionRepository:
    __connection: MongoClient
    __db: Database

    def __init__(self):
        self.__connection = MongoClient()
        self.__db = self.__connection['jobs']

    def save_one_job(self, collection_name: str, job_info: dict):
        self.__db[collection_name].insert_one(job_info)

    def jobs_count(self, collection_name: str):
        return self.__db[collection_name].count_documents({})

    def find_job_by_min_salary(self, collection_name: str, min_sal: int):
        return self.__db[collection_name].find(
            {'$and': [
                {'min_salary': {'$gt': min_sal}},
                {'max_salary': {'$gt': min_sal}}
            ]}
        )

    def __del__(self):
        self.__connection.close()
        print(f'Закрыл соединение с БД {self.__db.name}')
