FROM python:3.8-alpine

WORKDIR /app
COPY . /app

RUN apk update && apk add ffmpeg vim
RUN pip install -r requirements.txt

ENV APP_URL=https://drmsaw.beginners.seccon.games

CMD ["python", "./solver.py"]