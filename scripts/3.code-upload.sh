#!/bin/bash

source envs/.env

cd lambda-code

echo -e "UPLOADING CODE..."
aws --profile ${AWS_PROFILE_NAME} s3 cp code.zip "s3://$S3_BUCKET/code.zip"
