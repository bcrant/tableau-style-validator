#!/bin/bash

source envs/.env

echo -e "BUILDING CODE IMAGE..."
cd lambda-code
rm -rf code.zip

rm -rf python && mkdir -p python
docker run --rm -v $(pwd):/tmp -w /tmp lambci/lambda:build-${PYTHON_VERSION} bash -c \
  "arch && whoami && pip install -r requirements-code.txt -t ./python";

echo -e "ZIPPING CODE..."
zip -q -r code.zip . -x "*.pyc" "*.git" "*.sh" env.env out.json .DS_Store

#rm -rf python