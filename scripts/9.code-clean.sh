#!/bin/bash

source envs/.env

echo -e "REMOVING CURRENT ${LAMBDA_NAME} CONFIGURATION..."
aws --profile ${AWS_PROFILE_NAME} lambda delete-function \
  --function-name "${LAMBDA_NAME}"
