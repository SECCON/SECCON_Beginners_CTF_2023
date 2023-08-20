FROM python:3

COPY . .

ENV HOST=treasure.beginners.seccon.games
ENV PORT=13778

RUN pip install -U pwn

CMD ["python", "solve.py"]