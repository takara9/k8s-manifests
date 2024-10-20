## Alpine Linux 
FROM alpine:latest

## Node.js  https://pkgs.alpinelinux.org/package/edge/main/x86_64/nodejs
RUN apk update && apk add --no-cache nodejs npm

## 依存モジュールを同梱
WORKDIR /
ADD ./package.json /
RUN npm install


ADD ./webapl.js /
ADD ./public    /public


## アプリケーションの起動
CMD node /webapl.js
