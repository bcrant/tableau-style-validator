#!/bin/bash

source envs/.env

echo -e "UPDATING ${LAMBDA_NAME} CONFIGURATION..."

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
TABLEAU_PATH=${TABLEAU_PATH},\
STYLE_GUIDE_PATH=${STYLE_GUIDE_PATH},\
TABLEAU_WEBHOOK_URL=${TABLEAU_WEBHOOK_URL},\
WB_CREATED_WEBHOOK_NAME=${WB_CREATED_WEBHOOK_NAME},\
WB_CREATED_WEBHOOK_EVENT=${WB_CREATED_WEBHOOK_EVENT},\
WB_UPDATED_WEBHOOK_NAME=${WB_UPDATED_WEBHOOK_NAME},\
WB_UPDATED_WEBHOOK_EVENT=${WB_UPDATED_WEBHOOK_EVENT}\}


echo -e "SETTING LAMBDA RETRY POLICY..."
aws --profile ${AWS_PROFILE_NAME} lambda put-function-event-invoke-config \
  --function-name "${LAMBDA_NAME}" \
  --maximum-retry-attempts 0

LOG_GROUP_NAME=/aws/lambda/${LAMBDA_NAME}
echo -e "SETTING 14 DAY RETENTION PERIOD FOR CLOUDWATCH LOG GROUP: ${LOG_GROUP_NAME}"
aws --profile ${AWS_PROFILE_NAME} logs put-retention-policy \
  --log-group-name ${LOG_GROUP_NAME} \
  --retention-in-days 30
