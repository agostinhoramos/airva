#!/bin/bash

sudo apt-get install -y python3-venv
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env