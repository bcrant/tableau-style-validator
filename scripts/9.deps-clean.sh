#!/bin/bash

source envs/.env

echo -e "REMOVING CURRENT ${LAMBDA_LAYER_NAME} LAYER..."

while true; do

  LAMBDA_LAYER_VERSIONED=`aws --profile ${AWS_PROFILE_NAME} lambda list-layer-versions --layer-name ${LAMBDA_LAYER_NAME} --query 'max_by(LayerVersions, &Version).Version' --output text`
  echo -e "${LAMBDA_LAYER_VERSIONED}"

  if [ "None" = "${LAMBDA_LAYER_VERSIONED}" ]
  then
    break;
  fi

  aws --profile ${AWS_PROFILE_NAME} lambda delete-layer-version --layer-name ${LAMBDA_LAYER_NAME} --version-number ${LAMBDA_LAYER_VERSIONED} && sleep 2

done