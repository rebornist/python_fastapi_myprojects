# Pandas를 통해 excel파일 읽기
import pandas as pd

# excel파일 읽기
class ExcelHandler:
    def __init__(self, data):
        self.df = pd.read_excel(data)

    def read(self):
        return self.df

    def head(self, n: int):
        return self.df.head(n)

    def tail(self, n: int):
        return self.df.tail(n)

    def save(self, path, index=False):
        self.df.to_excel(path, index=index)