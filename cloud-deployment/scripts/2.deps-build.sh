#!/bin/bash

source envs/.env

echo -e "BUILDING DEPENDENCIES..."
cd lambda-deps
rm -rf validator-deps.zip

rm -rf python && mkdir -p python
docker run --rm -v $(pwd):/tmp -w /tmp lambci/lambda:build-${PYTHON_VERSION} bash -c \
  "arch \
  && whoami \
  && pip install -r requirements-deps.txt -t ./python \
  && echo -e 'ZIPPING LAYER ARTIFACTS AND CLOSING DOCKER RUNNER...' \
  && zip -q -r validator-deps.zip . -x '*.pyc' '*.git' '*.sh' env.env out.json .DS_Store \
  && arch \
  && whoami"

rm -rf python