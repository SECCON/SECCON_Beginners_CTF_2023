FROM python:3.11-alpine

RUN apk --no-cache add file socat
RUN adduser -D ctf

ADD polyglot4b.py /home/ctf/polyglot4b/polyglot4b.py
RUN chmod 500 /home/ctf/polyglot4b/polyglot4b.py
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf/polyglot4b/
CMD socat TCP-L:31416,fork,reuseaddr EXEC:"python3 -u polyglot4b.py",stderr