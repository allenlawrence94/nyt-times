#!/usr/bin/env bash
poetry version $(gitversion | jq -r .SemVer)
