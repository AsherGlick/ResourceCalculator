FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    procps pngquant xz-utils curl \
 && rm -rf /var/lib/apt/lists/*

ENV NODE_VERSION=18.20.4
RUN ARCH="$(uname -m)" && \
    case "$ARCH" in \
      x86_64) NODE_ARCH=x64 ;; \
      aarch64) NODE_ARCH=arm64 ;; \
      *) echo "unsupported arch: $ARCH" && exit 1 ;; \
    esac && \
    curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz" \
      -o /tmp/node.tar.xz && \
    tar -xJf /tmp/node.tar.xz -C /opt && \
    rm /tmp/node.tar.xz && \
    ln -sf /opt/node-v${NODE_VERSION}-linux-${NODE_ARCH}/bin/node /usr/local/bin/node && \
    ln -sf /opt/node-v${NODE_VERSION}-linux-${NODE_ARCH}/bin/node /usr/local/bin/nodejs && \
    ln -sf /opt/node-v${NODE_VERSION}-linux-${NODE_ARCH}/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

WORKDIR /usr/src/app
ENTRYPOINT ["/usr/src/app/dockerfiles/build.sh"]
