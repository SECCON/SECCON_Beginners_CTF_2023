FROM python:3.8-alpine

WORKDIR /app
ADD . /app

ENV ENDPOINT=https://phisher2.beginners.seccon.games
ENV ACCESS_TOKEN=b429846ef7ef504b02ff879f3547f469

RUN pip install -r requirements.txt

CMD ["python", "/app/solver.py"]