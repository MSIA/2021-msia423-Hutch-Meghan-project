#!/usr/bin/env bash

# download data from s3
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY mrh1996 run.py --connect_type='download' --s3path='s3://2021-msia423-hutch-meghan/data/tweets.csv' --local_path='data/external/constructs.csv' --s3='s3'

# train lda model
docker run mrh1996 model.py

