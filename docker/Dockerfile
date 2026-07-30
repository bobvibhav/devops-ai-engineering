FROM python:3.13-slim

WORKDIR /app

COPY app.py .

RUN pip install requests

CMD [ "python", "app.py" ]