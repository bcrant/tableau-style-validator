#!/bin/bash

source envs/.env

echo -e "GETTING CURRENT ${LAMBDA_NAME} CONFIGURATION..."
aws --profile ${AWS_PROFILE_NAME} lambda get-function-configuration --function-name "${LAMBDA_NAME}"