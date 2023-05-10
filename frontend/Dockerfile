FROM node:16.14.0

RUN npm config set registry https://registry.npm.taobao.org

ENV FRONTEND=/opt/frontend

WORKDIR $FRONTEND

COPY package.json $FRONTEND
COPY package-lock.json $FRONTEND
RUN npm install

COPY . $FRONTEND
RUN npm run build


FROM nginx:1.20.2
EXPOSE 80

COPY --from=0 /opt/frontend/dist/ usr/share/nginx/html
ENTRYPOINT nginx -g "daemon off;"
