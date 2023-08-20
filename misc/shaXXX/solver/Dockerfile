FROM python:3

COPY . .

ENV HOST=shaxxx.beginners.seccon.games
ENV PORT=25612

RUN pip install -U pwn

CMD ["python", "solver.py"]
