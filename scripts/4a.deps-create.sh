#!/bin/bash

source envs/.env

echo -e "CREATING LAMBDA LAYER ${LAMBDA_LAYER}"
aws --profile ${AWS_PROFILE_NAME} lambda publish-layer-version \
  --layer-name ${LAMBDA_LAYER} \
  --compatible-runtimes ${PYTHON_VERSION} \
  --content S3Bucket=${S3_BUCKET},S3Key=alldeps.zip
