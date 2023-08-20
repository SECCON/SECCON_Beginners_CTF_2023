FROM alpine:latest

WORKDIR /home/ctf/shaXXX

COPY main.py flag.py .

RUN apk update && \
    apk upgrade && \
    apk add --no-cache socat python3

CMD socat TCP-L:44322,fork,reuseaddr EXEC:"python3 ./main.py",stderr
