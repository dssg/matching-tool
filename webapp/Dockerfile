FROM python:3.6

RUN apt-get -y update && \
	apt-get install unzip sudo

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app

ADD ./setup.py /user/src/app/setup.py

RUN pip install --editable .


ENV PYTHONPATH /usr/src/app
ENV FLASK_APP app
ENV FLASK_DEBUG true

CMD flask run --host=0.0.0.0
