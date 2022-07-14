#!/bin/bash

version=$(eval "curl --version");
if [ -z "$version" ]; then
    sudo apt install -y curl;
fi

version=$(eval "python --version");
if [ -z "$version" ]; then
    alias python=python3;
fi

version=$(eval "poetry --version");
if [ -z "$version" ]; then
    sudo apt-get install -y python3-venv
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    source $HOME/.poetry/env
else
    echo "Poetry already installed :)"
fi