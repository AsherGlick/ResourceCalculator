# Get the user and group id which the docker compose config will use to access
# the mounted directory with the correct user.
export UID=`id -u`
export GID=`id -g`

# Convert the arguments into a quoted string array to pass into an environment
# variable that will then be used as command line arguments for build.py.
arguments=""
for var in "$@"
do
    arguments=$arguments" \"$var\""
done
export arguments

# Run docker compose
docker-compose up
