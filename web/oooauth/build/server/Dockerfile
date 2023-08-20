FROM node:20-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm i

COPY . .

RUN adduser -D server
USER server

CMD ["npm", "start"]