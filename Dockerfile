FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./src/s3_upload.py /app/s3_upload.py

COPY ./src/add_tweets.py /app/add_tweets.py

COPY ./run.py /app/run.py

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3"]
