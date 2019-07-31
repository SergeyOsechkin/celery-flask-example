FROM python:3.7-alpine

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt --no-cache-dir

COPY . /app
WORKDIR /app

CMD ["flask", "run"]
