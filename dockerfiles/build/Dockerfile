FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    procps \
    pngquant \
    npm \
    curl \
 && rm -rf /var/lib/apt/lists/*

# # Install NVM and NodeJS the official way (requries an interactive posix shell for some demonic reason)
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# ENV NVM_DIR=/root/.nvm
# ENV NODE_VERSION=18
# RUN . $NVM_DIR/nvm.sh && \
#     nvm install $NODE_VERSION && \
#     nvm use v$NODE_VERSION && \
#     nvm alias default $NODE_VERSION
# ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

# Install FNM and NodeJS an alternative way (the pip-to-bash install bs just fails)
# RUN curl -fsSL https://fnm.vercel.app/install | bash
# RUN fnm use --install-if-missing 18

# A chaotic, but working method of installing node18 via n, installed with an older version of node
RUN npm cache clean -f
RUN npm install -g n
RUN n 18

WORKDIR /usr/src/app

ENTRYPOINT ["/usr/src/app/dockerfiles/build.sh"]
