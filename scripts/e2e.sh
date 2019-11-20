#!/usr/bin/env bash
set -e
docker-compose -f docker-compose.yml -f scripts/docker-compose.e2e.yml build
docker-compose -f docker-compose.yml -f scripts/docker-compose.e2e.yml run client || \
    docker-compose -f docker-compose.yml -f scripts/docker-compose.e2e.yml down
docker-compose -f docker-compose.yml -f scripts/docker-compose.e2e.yml down
