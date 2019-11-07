#!/usr/bin/env bash
docker-compose -f docker-compose.yml -f scripts/docker-compose.test.yml build
docker-compose -f docker-compose.yml -f scripts/docker-compose.test.yml run app
rc=$?
docker-compose -f docker-compose.yml -f scripts/docker-compose.test.yml down
exit $rc
