FROM node:12.6

ADD . /root/project
WORKDIR /root/project

RUN \
    node --version && \
    npm --version && \
    yarn --version && \
    yarn config set registry http://mirrors.cloud.tencent.com/npm/ && \
    echo done

RUN \
    yarn install && \
    echo done
