#!/bin/bash

source envs/.env

echo -e "UPDATING ${LAMBDA_NAME} CONFIGURATION..."

echo -e "GETTING DATABASE HOSTNAME..."
DB_HOST=`aws --profile ${AWS_PROFILE_NAME} rds describe-db-instances --db-instance-identifier ${DB_INSTANCE_NAME} --query "DBInstances[*].Endpoint.Address" --output text`
echo -e "${DB_HOST}"

echo -e "GETTING LAYER VERSION HOSTNAME..."
LAMBDA_LAYER_VERSIONED=`aws --profile ${AWS_PROFILE_NAME} lambda list-layer-versions --layer-name ${LAMBDA_LAYER_NAME} --query 'max_by(LayerVersions, &Version).LayerVersionArn' --output text`
echo -e "${LAMBDA_LAYER_VERSIONED}"

echo -e "GETTING LAMBDA ARN..."
LAMBDA_ARN=`aws --profile ${AWS_PROFILE_NAME} lambda get-function-configuration --function-name "${LAMBDA_NAME}" --query 'FunctionArn' --output text`
echo -e "${LAMBDA_ARN}"

echo -e "SETTING LAMBDA CONFIGURATION..."
aws --profile ${AWS_PROFILE_NAME} lambda update-function-configuration \
  --function-name "${LAMBDA_NAME}" \
  --timeout ${LAMBDA_TIMEOUT} \
  --memory-size ${LAMBDA_MEMORY_SIZE} \
  --layers ${LAMBDA_LAYER_VERSIONED} \
  --environment Variables=\{\
LAMBDA_MEMORY_SIZE=${LAMBDA_MEMORY_SIZE},\
TABLEAU_USER=${TABLEAU_USER},\
TABLEAU_PASS=${TABLEAU_PASS},\
TABLEAU_SERVER_URL=${TABLEAU_SERVER_URL},\
TABLEAU_SITE_NAME=${TABLEAU_SITE_NAME},\
TABLEAU_VIEW=${TABLEAU_VIEW},\
TABLEAU_PATH=${TABLEAU_PATH},\
SLACK_CHANNEL=${SLACK_CHANNEL},\
SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}\}


echo -e "SETTING LAMBDA RETRY POLICY..."
aws --profile ${AWS_PROFILE_NAME} lambda put-function-event-invoke-config \
  --function-name "${LAMBDA_NAME}" \
  --maximum-retry-attempts 0

# The generate-cli-skeleton produces a json structure that can't be re-used, so we're going to just
# pull out the pieces we need to update this API and write this string to a temp file to avoid all the escaping malarky.
CONTRIVED_EVENTBRIDGE_RULE_TARGET_JSON="{\"Rule\": \"\",\"Targets\": [{\"Arn\": \"\",\"Input\": \"\"}]}"
echo -e "ATTACHING LAMBDA ${LAMBDA_ARN} TO ${EVENTBRIDGE_CRON_NAME}..."
echo ${CONTRIVED_EVENTBRIDGE_RULE_TARGET_JSON} \
    | jq ".Targets[0].Input=\"${LAMBDA_EVENT_DATA}\"" \
    | jq ".Targets[0].Id=\"1\"" \
    | jq ".Targets[0].Arn=\"${LAMBDA_ARN}\"" \
    | jq ".Rule=\"${EVENTBRIDGE_CRON_NAME}\"" \
    > /tmp/update.cli.json
aws --profile ${AWS_PROFILE_NAME} events put-targets --cli-input-json file:///tmp/update.cli.json
rm /tmp/update.cli.json

LOG_GROUP_NAME=/aws/lambda/${LAMBDA_NAME}
echo -e "SETTING 14 DAY RETENTION PERIOD FOR CLOUDWATCH LOG GROUP: ${LOG_GROUP_NAME}"
aws --profile ${AWS_PROFILE_NAME} logs put-retention-policy \
  --log-group-name ${LOG_GROUP_NAME} \
  --retention-in-days 30
