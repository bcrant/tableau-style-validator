#!/bin/bash

source envs/.env

echo -e "BUILDING DEPENDENCIES..."
cd lambda-deps
rm -rf alldeps.zip

rm -rf python && mkdir -p python
docker run --rm -v $(pwd):/tmp -w /tmp amazon/aws-lambda-python:latest --platform linux/arm64/v8 pip install -r requirements-deps.txt -t ./python;
echo -e "ZIPPING LAYER ARTIFACTS..."
zip -q -r alldeps.zip . -x "*.pyc" "*.git" "*.sh" env.env out.json .DS_Store

#rm -rf python