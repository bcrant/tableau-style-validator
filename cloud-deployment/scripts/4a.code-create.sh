#!/bin/bash

source envs/.env

echo -e "CREATING LAMBDA FUNCTION ${LAMBDA_NAME}..."
aws --profile ${AWS_PROFILE_NAME} lambda create-function \
  --function-name ${LAMBDA_NAME} \
  --runtime ${PYTHON_VERSION} \
  --code S3Bucket=${S3_BUCKET},S3Key=code.zip \
  --handler ${LAMBDA_HANDLER} \
  --role arn:aws:iam::${IAM_ACCOUNT}:role/${IAM_LAMBDA_ROLE}