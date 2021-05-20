from database_config import config
import pymysql


class DatabaseConnection:
    def __init__(self):
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def get_connection(self):
        connection = pymysql.connect(
            user=self.user, passwd=self.password, host=self.host, database=self.database)
        return connection

    def __enter__(self):
        return self

    def __exit__(self):
        pass
