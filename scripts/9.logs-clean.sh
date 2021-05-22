#!/bin/bash

source envs/.env

echo -e "DELETING CLOUDWATCH LOG GROUP FOR LAMBDA FUNCTION ${LAMBDA_NAME}"
LOG_GROUP_NAME=/aws/lambda/${LAMBDA_NAME}
aws --profile ${AWS_PROFILE_NAME} logs delete-log-group \
  --log-group-name ${LOG_GROUP_NAME}
