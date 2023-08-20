FROM python:3

ENV DEBIAN_FRONTEND nointeractive
RUN apt-get update && apt-get install -yqq libyara-dev

WORKDIR /app
ADD . /app
RUN pip install -r requestments.txt

ENV PWNLIB_NOTERM true
ENV CTF4B_HOST=yaro.beginners.seccon.games
ENV CTF4B_PORT=5003

CMD ["python3", "solve.py"]
