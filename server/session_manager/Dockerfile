FROM python:3.9

EXPOSE 8888

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt  #--no-cache-dir

COPY . .

ENTRYPOINT ["python3", "main.py"]
