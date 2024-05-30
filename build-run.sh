#!/bin/sh
WD=`dirname $0`

#docker rmi -f feilong/bit-trader-crawler-news-ai
private_host=$(python3 ip-util.py 2>&1)
export redis_host=$private_host
echo $redis_host

cd $WD && docker build -f Dockerfile -t feilong/crawler-news-ai .

docker-compose -p crawler -f docker-compose-crawler-news-ai.yaml up -d
