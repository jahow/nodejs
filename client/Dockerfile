FROM node:10.14.1

RUN mkdir -p /app/client
WORKDIR /app/client

COPY package*.json /app/client/

RUN npm install

COPY . /app/client

EXPOSE 3000
