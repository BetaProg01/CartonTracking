#!/bin/bash
cd infra/consumer/
export BROKER_IP="$1" # localhost if empty
docker compose up -d --build