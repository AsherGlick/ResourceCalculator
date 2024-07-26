FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    procps \
    pngquant \
    xz-utils \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Download and install Node.js version 18
ENV NODE_VERSION=18.20.4
RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz -o node-v${NODE_VERSION}-linux-x64.tar.xz && \
    tar -xJvf node-v${NODE_VERSION}-linux-x64.tar.xz -C /opt/ && \
    rm node-v${NODE_VERSION}-linux-x64.tar.xz
RUN ln -s /opt/node-v${NODE_VERSION}-linux-x64/bin/node /usr/local/bin/node
RUN ln -s /opt/node-v${NODE_VERSION}-linux-x64/bin/node /usr/local/bin/nodejs
RUN ln -s /opt/node-v${NODE_VERSION}-linux-x64/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

WORKDIR /usr/src/app

ENTRYPOINT ["/usr/src/app/dockerfiles/build.sh"]
