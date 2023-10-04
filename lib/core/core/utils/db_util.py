import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker, session


class DbHelper:
    def __init__(self, db_name: str = os.environ["POSTGRES_DB"]):
        self.db_name = db_name
        self.db_host = os.environ["POSTGRES_HOST"]
        self.db_user = os.environ["POSTGRES_USER"]
        self.db_pass = os.environ["POSTGRES_PASSWORD"]
        self.db_port = os.environ["POSTGRES_PORT"]

    @property
    def connection_string(self):
        return f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_connection(self) -> session:
        engine = sqlalchemy.create_engine(self.connection_string)
        return sessionmaker(engine)
