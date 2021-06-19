#!/bin/bash

source envs/.env

# Adjust the read timeout by +30 seconds to allow us to wait the full remote execution timeout period.
READ_TIMEOUT=$(expr 30 + $LAMBDA_TIMEOUT)

echo -e "Invoking Lambda with LAMBDA_EVENT_DATA and..."
echo ${LAMBDA_EVENT_DATA} | sed 's/\\"/"/g' | jq -c > /tmp/update.cli.json
jq -C -c < /tmp/update.cli.json
echo -e "... waiting for ${READ_TIMEOUT} seconds maximum..."

aws --profile ${AWS_PROFILE_NAME} lambda invoke --function-name "${LAMBDA_NAME}" \
                  --cli-read-timeout ${READ_TIMEOUT} \
                  --cli-connect-timeout 30 \
                  /tmp/aws.out.json \
                  --log-type Tail \
                  --payload file:///tmp/update.cli.json &

LOG_GROUP_NAME=/aws/lambda/${LAMBDA_NAME}
echo -e "Beginning real-time stream of Cloudwatch log for ${LOG_GROUP_NAME}..."
awslogs get ${LOG_GROUP_NAME} ALL --watch --profile ${AWS_PROFILE_NAME}

