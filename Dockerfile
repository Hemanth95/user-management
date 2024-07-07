
FROM python:3.12-slim

WORKDIR /app

COPY alembic /app/alembic

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

COPY alembic.ini /app/alembic.ini

COPY wait-for-it.sh /app/wait-for-it.sh

COPY prepopulate_db.py /app/prepopulate_db.py

COPY start_app.sh /app/start_app.sh

RUN chmod +x /app/start_app.sh

RUN chmod +x /app/wait-for-it.sh 

