FROM python:3.11-alpine

RUN apk --no-cache add file socat
RUN adduser -D ctf

ADD polyglot4b2.py /home/ctf/polyglot4b2/polyglot4b2.py
RUN chmod 500 /home/ctf/polyglot4b2/polyglot4b2.py
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf/polyglot4b2/
CMD socat TCP-L:31417,fork,reuseaddr EXEC:"python3 -u polyglot4b2.py",stderr