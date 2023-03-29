import psycopg2

from lib.get_config import GetConfig


# DB connection
class DBConnection:
    __config = GetConfig('config.yml').get_config()['db']['postgres']

    # 초기화
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.database: str = database

    def get_config(self):
        return self.__config

    def postgresql(self) -> psycopg2:
        return psycopg2.connect(
            host=self.get_config()['host'],
            port=self.get_config()['port'],
            user=self.get_config()['user'],
            password=self.get_config()['password'],
            database=self.get_config()['database'],
        )

