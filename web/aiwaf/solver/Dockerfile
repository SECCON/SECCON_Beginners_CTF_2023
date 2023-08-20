FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY . .

CMD ["bash", "solver.sh"]
