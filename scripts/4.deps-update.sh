#!/bin/bash

source envs/.env

echo -e "UPDATING LAMBDA LAYER ${LAMBDA_LAYER_NAME}..."
aws --profile ${AWS_PROFILE_NAME} lambda publish-layer-version \
  --layer-name ${LAMBDA_LAYER_NAME} \
  --compatible-runtimes ${PYTHON_VERSION} \
  --content S3Bucket=${S3_BUCKET},S3Key=validator-deps.zip