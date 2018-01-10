FROM python:3.6.2

RUN mkdir -p /csh/matcher
WORKDIR /csh

ADD requirements.txt /csh/requirements.txt

RUN pip install -r requirements.txt

ADD matcher /csh/matcher

ADD setup.py /csh/setup.py

RUN pip install --editable .

ENV FLASK_APP matcher.api
ENV FLASK_DEBUG true

CMD flask run --host=0.0.0.0
