import pandas as pd

# 파일 pandas로 읽은 후 컬럼 수정하기
def read_excel(file):
    # 엑셀 파일 읽기
    df = pd.read_excel(file)
    # 컬럼명 추출
    columns = df.columns

    # 컬럼명 수정
    for i, col in enumerate(columns):
        df.rename(columns={col: f"col_{i}"}, inplace=True)

    print(df.head())


if __name__ == "__main__":
    read_excel("C:\\Users\\rdid-ss\\Downloads\\[완료]08. 대전광역시 서구_경찰서 현황 (1).xlsx")