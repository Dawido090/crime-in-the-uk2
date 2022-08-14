from sqlalchemy import (create_engine,MetaData,Table, Column, Integer, Numeric, String,
                ForeignKey, DateTime, PrimaryKeyConstraint,
                UniqueConstraint, CheckConstraint, Boolean, Constraint, select)

from datetime import datetime
import pymongo


#postgresql://username:password@host:port/dbname[?paramspec]

class PostgresDataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('article_id', Integer(), primary_key=True, autoincrement=True),
        Column('mongo_id', String(), primary_key=True),
        Column('title',String(),nullable=False),
        Column('post_date',DateTime(),nullable=False),
        Column('link',String(),nullable=False),
        Column('content',String(),nullable=False)

        )
    most_wanted = Table('most_wanted', metadata,
        Column('article_id', Integer(), primary_key=True, autoincrement=True),
        Column('mongo_id', String(), primary_key=True),
        Column('title',String(),nullable=False),
        Column('link',String(),nullable=False),
        Column('content',String(),nullable=False)

        )

    def db_init(self):
        conn_string = "postgresql+psycopg2://app_user:abc123@postgres_final:5432/postgres" #container
        # conn_string = "postgresql+psycopg2://app_user:abc123@localhost:5432/postgres" #local
        self.engine = create_engine(conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
    
PostgresDal = PostgresDataAccessLayer()


class MongoDataAccessLayer:
    # add os.env
    host = None
    username = None
    password = None
    connection = None

    def __init__(self, host):        
        self.host = host,

    def mongo_init(self):
        self.connection = pymongo.MongoClient(
            host = self.host,
        )
          
    
MongoDal = MongoDataAccessLayer("mongodb://root:abc123@mongo_raw") #for container
# MongoDal = MongoDataAccessLayer("mongodb://root:abc123@127.0.0.1:27018") #for local