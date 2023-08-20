FROM python:3.8-slim-buster

RUN mkdir /var/www
WORKDIR /var/www
COPY app.py admin.py requirements.txt uwsgi.ini index.html .
RUN mkdir images uploads

# install dependencies
RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
    gcc libgdal-dev \
    tesseract-ocr wget curl unzip \
    gnupg gnupg2 gnupg1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

RUN chmod 744 -R /var/www
RUN chown -R www-data:www-data /var/www
USER www-data

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]