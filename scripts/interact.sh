#!/usr/bin/env bash
set -e
CONTAINER=${1:-"app"}
docker-compose -f docker-compose.yml -f scripts/docker-compose.dev.yml build
{
    docker-compose -f docker-compose.yml -f scripts/docker-compose.dev.yml up -d
    docker exec -it "${CONTAINER}" /bin/bash
} || {
    docker-compose -f docker-compose.yml -f scripts/docker-compose.dev.yml down
}
docker-compose -f docker-compose.yml -f scripts/docker-compose.dev.yml down
