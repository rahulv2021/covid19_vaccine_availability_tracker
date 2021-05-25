from config.database import connection_string
import pymysql


class DatabaseConnection:
    def __init__(self):
        self.host = connection_string["host"]
        self.user = connection_string["user"]
        self.password = connection_string["password"]
        self.database = connection_string["database"]

    def get_connection(self):
        connection = pymysql.connect(
            user=self.user, passwd=self.password, host=self.host, database=self.database)
        return connection

    def __enter__(self):
        return self

    def __exit__(self):
        pass
