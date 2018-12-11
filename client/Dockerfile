FROM node:10.14.1

RUN mkdir -p /app/client
WORKDIR /app/client

COPY angular-docker/package*.json /app/client/
COPY angular-docker /app/client
RUN npm install -g @angular/cli
RUN npm install

EXPOSE 4200
