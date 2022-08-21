#! /bin/bash

# if [ "$UID" -eq 0 ]
#   then echo "This is running as root but probably should not be"
#   exit
# fi


echo $UID : $GID

# Install or update all dependencies.
npm install
if [ ! -d "venv_docker" ]; then python3 -m venv venv_docker; fi
source venv_docker/bin/activate
pip install --quiet --no-cache-dir --requirement requirements.txt

# Run the build script.
echo "ARGS:" "$@"
python -u build.py "$@"
