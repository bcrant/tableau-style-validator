#!/bin/bash

source envs/.env

# PRINT MOST RECENT CLOUDWATCH LOG TO TERMINAL
# (COMPLETED INVOCATIONS ONLY, NOT LIVE TIME)

LOG_GROUP_NAME=/aws/lambda/${LAMBDA_NAME}

echo -e "GETTING LATEST LAMBDA INVOCATION FROM CLOUDWATCH FOR LOG GROUP: ${LOG_GROUP_NAME}..."
LOG_STREAM_NAME=$(aws --profile ${AWS_PROFILE_NAME} logs describe-log-streams \
  --log-group-name ${LOG_GROUP_NAME} \
  --order-by 'LastEventTime' \
  --max-items 1 \
  --descending \
  --query 'logStreams[0].logStreamName' |
  jq -r)

echo -e "PRINTING LATEST CLOUDWATCH STREAM FOR LOG GROUP: ${LOG_STREAM_NAME}"
aws --profile ${AWS_PROFILE_NAME} logs get-log-events \
  --log-group-name ${LOG_GROUP_NAME} \
  --log-stream-name ${LOG_STREAM_NAME} \
  --query events[*].message \
  --output json |
  jq -C
