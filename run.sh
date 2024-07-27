# Get the user and group id which the docker compose config will use to access
# the mounted directory with the correct user.
export TARGET_UID=`id -u`
export TARGET_GID=`id -g`

echo "run.sh UID:GID ${TARGET_UID}:${TARGET_GID}"

# Create the output directory as the current user to avoid a race condition
# where the webserver will create the directory as root if it launches before
# the build process is able to create the folder as the correct user.
mkdir -p output

# Convert the arguments into a quoted string array to pass into an environment
# variable that will then be used as command line arguments for build.py.
arguments=""
for var in "$@"
do
    arguments=$arguments" \"$var\""
done
export arguments

# Run docker compose
docker ps > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Running docker-compose with sudo"
    sudo -E docker-compose up --build
else
    docker-compose up --build
fi
