FROM python:3.6.2

RUN mkdir -p /csh/matcher
WORKDIR /csh/matcher

ADD requirements.txt /csh/matcher/requirements.txt

RUN pip install -r requirements.txt

ADD . /csh/matcher

ADD setup.py /csh/matcher/setup.py

RUN pip install --editable .

ENV PYTHONPATH /csh/matcher
ENV FLASK_APP matcher.api
ENV FLASK_DEBUG true

CMD flask run --host=0.0.0.0
