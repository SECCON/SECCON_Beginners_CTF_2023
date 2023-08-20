FROM python:3

COPY . .

RUN apt-get update && apt-get install -y netcat

ENV HOST=polyglot4b2.beginners.seccon.games
ENV PORT=31417

CMD ["/bin/sh", "solver.sh"]
