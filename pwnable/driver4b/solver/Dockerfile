FROM python:3

RUN apt-get update && apt-get install -y hashcash
RUN pip install -U pwn

WORKDIR /app
ADD . /app

ENV PWNLIB_NOTERM true

CMD ["python3", "solve.py"]
