#!/bin/bash
cd infra/producer/

export BROKER_IP="$1"
export PRODUCER_NUMBER="$2"
export ITERATIONS="$3"
export ITERATION_GAP="$4"

docker compose up -d --build