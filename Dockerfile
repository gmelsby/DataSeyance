FROM python:3.6-slim-buster

WORKDIR /data-seyance

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install libmariadbclient-dev gcc -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]