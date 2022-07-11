FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    procps \
    pngquant \
    npm \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ENTRYPOINT ["/usr/src/app/dockerfiles/build.sh"]
