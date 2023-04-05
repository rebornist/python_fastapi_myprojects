# 공식 Python 이미지를 베이스로 지정
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 목록 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY . .

# 80 포트로 서비스
EXPOSE 80

# uvicorn 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]