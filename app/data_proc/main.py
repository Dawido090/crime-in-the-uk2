try: from .base import PostgresDal
except: pass
try: from base import PostgresDal
except: pass
from datetime import datetime
from sqlalchemy import select
try: from .base import MongoDal
except: pass
try: from base import MongoDal
except: pass
import time
from pymongo import errors, MongoClient

class MongoDataProc:     
    
    def __init__(self, client):
        self.client = client

    def check_connection(self) -> None:
        """
        Validator - checks connection for DELAY_LITERATIONS*DELAY_UNIT seconds
        if there is a reconnection to the database. If not, raise error.
        """

        DELAY_LITERATIONS = 10 #loops
        DELAY_UNIT = 1 #Sec per iteration

        for _ in range(DELAY_LITERATIONS):
            time.sleep(DELAY_UNIT)
            try:
                self.mongo_client.server_info()
            except errors.ServerSelectionTimeoutError:
                MongoDal.mongo_init()
            else:
                break
        try:
            self.mongo_client.server_info()
        except errors.ServerSelectionTimeoutError as error:
            raise error


    def connection(self) -> MongoClient:
        """
        Connection to mongo db with checker, which checks connection status
        """
        self.check_connection()
        return self.mongo_client

    def get_articles_data(self):
        db = self.client["web_content"]
        col = db["articles"]
        data = col.find({},{})
        all_links = [x for x in data]
        return all_links
    
    def get_most_wanted_data(self):
        db = self.client["web_content"]
        col = db["most_wanted"]
        data = col.find({},{})
        all_links = [x for x in data]
        return all_links


class PostgresDataProc:     
    

    def __init__(self, client):
        self.client = client

    # def check_connection(self) -> None:
    #     """
    #     Validator - checks connection for DELAY_LITERATIONS*DELAY_UNIT seconds
    #     if there is a reconnection to the database. If not, raise error.
    #     """

    #     DELAY_LITERATIONS = 10 #loops
    #     DELAY_UNIT = 1 #Sec per iteration

    #     for _ in range(DELAY_LITERATIONS):
    #         time.sleep(DELAY_UNIT)
    #         try:
    #             self.mongo_client.server_info()
    #         except errors.ServerSelectionTimeoutError:
    #             MongoDal.mongo_init()
    #         else:
    #             break
    #     try:
    #         self.mongo_client.server_info()
    #     except errors.ServerSelectionTimeoutError as error:
    #         raise error


    # def connection(self) -> MongoClient:
    #     """
    #     Connection to mongo db with checker, which checks connection status
    #     """
    #     self.check_connection()
    #     return self.mongo_client


    def add_article(self, mongo_id:str, title:str, post_date:datetime, link:str, content:str):
        ins = self.client.articles.insert()

        self.client.connection.execute(ins,
            mongo_id = mongo_id,
            title = title,
            post_date = post_date,
            link = link,
            content = content
        )
    
    def add_most_wanted(self, mongo_id:str, title:str, link:str, content:str):
        ins = self.client.articles.insert()

        self.client.connection.execute(ins,
            mongo_id = mongo_id,
            title = title,
            link = link,
            content = content
        )

    def get_article(self):
        result = []
        sel = self.client.articles.select()
        for i in self.client.connection.execute(sel).fetchall():
            result.append(i)
        return result

class Data_Proc_Class:
    def __init__(self, mongo_proc, postgres_proc) -> None:
        self.mongo_proc = mongo_proc
        self.postgres_proc = postgres_proc

    def main(self):
        mongo_data = self.mongo_proc.get_articles_data()
        print(mongo_data)


if __name__ == '__main__':
    time.sleep(15)
    if MongoDal.connection == None:
        MongoDal.mongo_init()
    
    if PostgresDal.connection == None:
        PostgresDal.db_init()


    mongo_proc = MongoDataProc(MongoDal.connection)
    postgres_proc = PostgresDataProc(PostgresDal)

    Data_Proc_Process = Data_Proc_Class(mongo_proc,postgres_proc)
    Data_Proc_Process.main()
    # print(postgres_proc.get_article())
