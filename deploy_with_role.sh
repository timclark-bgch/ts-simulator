#!/usr/bin/env bash

echo $DEPLOY_ROLE_ARN

CREDS=$(aws sts assume-role --role-arn \
  $DEPLOY_ROLE_ARN \
  --role-session-name my-sls-session --out json)
export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $CREDS | jq -r '.Credentials.SessionToken')

echo $@
$@