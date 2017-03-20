#!/usr/bin/env bash

npm install -g serverless

serverless deploy
serverless info > team_deploy.txt