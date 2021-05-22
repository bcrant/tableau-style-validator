#!/bin/bash

source envs/.env

cd lambda-deps

echo -e "UPLOADING DEPS..."
aws --profile ${AWS_PROFILE_NAME} s3 cp alldeps.zip "s3://$S3_BUCKET/alldeps.zip"
