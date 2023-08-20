FROM node:19-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
COPY index.js ./
RUN npm i

RUN adduser -D ctf4b
USER ctf4b

CMD ["node", "index.js"]
