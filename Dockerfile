FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN python setup.py

CMD ["python", "./main.py"]
