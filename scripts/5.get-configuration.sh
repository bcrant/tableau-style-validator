#!/bin/bash

source envs/.env

echo -e "GETTING CURRENT ${LAMBDA_NAME} CONFIGURATION..."
aws --profile ${AWS_PROFILE_NAME} lambda get-function-configuration --function-name "${LAMBDA_NAME}"

echo -e "GETTING DATABASE HOSTNAME..."
DB_HOST=`aws --profile ${AWS_PROFILE_NAME} rds describe-db-instances --db-instance-identifier ${DB_INSTANCE_NAME} --query "DBInstances[*].Endpoint.Address" --output text`
echo -e "${DB_HOST}"

if test -z "$NAT_INSTANCE_ENDPOINT"
then
  echo -e "GETTING NAT INSTANCE IP ADDRESS FOR ${NAT_INSTANCE_ID}..."
  NAT_INSTANCE_ENDPOINT=`aws --profile ${AWS_PROFILE_NAME} ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress[]" --instance-ids ${NAT_INSTANCE_ID} --output=text`
  echo ${NAT_INSTANCE_ENDPOINT}
else
  echo -e "USING PRECONFIGURED NAT_INSTANCE_ENDPOINT ${NAT_INSTANCE_ENDPOINT}..."
fi

echo -e "GETTING EVENTBRIDGE RULE ${EVENTBRIDGE_CRON_NAME}..."
aws --profile ${AWS_PROFILE_NAME} events describe-rule --name "${EVENTBRIDGE_CRON_NAME}"

echo -e "LISTING RULE TARGETS FOR ${EVENTBRIDGE_CRON_NAME}..."
aws --profile ${AWS_PROFILE_NAME} events list-targets-by-rule --rule "${EVENTBRIDGE_CRON_NAME}"
