# Pandas를 통해 csv파일 읽기

import pandas as pd
from typing import Any
from io import StringIO

# csv파일 읽기
class CsvHandler:
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def read(self):
        return self.df

    def head(self, n: int):
        return self.df.head(n)

    def tail(self, n: int):
        return self.df.tail(n)

    def save(self, path, index=False):
        self.df.to_csv(path, index=index)


