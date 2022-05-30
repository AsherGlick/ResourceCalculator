#! /bin/bash

# Install or update all dependencies.
npm install
if [ ! -d "venv_docker" ]; then python3 -m venv venv_docker; fi
source venv_docker/bin/activate
pip install --quiet --no-cache-dir --requirement requirements.txt

# Run the build script.
python -u build.py "$@"
