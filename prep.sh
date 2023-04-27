#!/usr/bin/env bash
version=$(toml get --toml-path pyproject.toml tool.poetry.version)
starting_commit=$1
poetry run auto-changelog --stdout -v $version --starting-commit $starting_commit																			