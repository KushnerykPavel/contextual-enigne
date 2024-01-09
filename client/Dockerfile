FROM node:18-alpine as build

RUN mkdir -p /usr/app
WORKDIR /usr/app
COPY . /usr/app

ARG REACT_APP_HTTP_URL

ENV REACT_APP_HTTP_URL $REACT_APP_HTTP_URL

ARG REACT_APP_WS_URL

ENV REACT_APP_WS_URL $REACT_APP_WS_URL

RUN npm install
RUN npm run build

FROM nginx:1.23.1-alpine
EXPOSE 3000
COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY --from=build /usr/app/build /usr/share/nginx/html