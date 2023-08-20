FROM python:3.11-alpine

RUN apk --no-cache add socat
RUN adduser -D ctf

ADD server.py /home/ctf/server.py
ADD FLAG      /home/ctf/flag
ADD requirements.txt /home/ctf/requirements.txt
RUN pip install -r /home/ctf/requirements.txt
RUN chmod 500 /home/ctf/server.py
RUN chmod 400 /home/ctf/flag
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf/
CMD socat TCP-L:13778,fork,reuseaddr EXEC:"python3 ./server.py",stderr
