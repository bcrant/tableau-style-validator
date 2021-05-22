#!/bin/bash

source envs/.env

echo -e "UPDATING LAMBDA CODE ${LAMBDA_NAME}..."
aws --profile ${AWS_PROFILE_NAME} lambda update-function-code \
  --function-name "${LAMBDA_NAME}" \
  --s3-bucket $S3_BUCKET \
  --s3-key code.zip
