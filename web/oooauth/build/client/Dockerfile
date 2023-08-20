FROM node:20-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm i

COPY . .

RUN adduser -D client
USER client

CMD ["npm", "start"]