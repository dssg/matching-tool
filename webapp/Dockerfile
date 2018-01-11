FROM python:3.6

RUN apt-get -y update && \
	apt-get install unzip sudo

RUN mkdir -p /csh/webapp
WORKDIR /csh/webapp

ADD requirements.txt /csh/webapp/requirements.txt
ADD requirements_dev.txt /csh/webapp/requirements_dev.txt
ADD README.md /csh/webapp/README.md

RUN pip install -r requirements.txt


ADD . /csh/webapp
ADD config.yaml /csh/webapp/config.yaml
ADD setup.py /csh/webapp/setup.py

RUN pip install --editable .

ENV PYTHONPATH /csh/webapp
ENV FLASK_APP webapp.app
ENV FLASK_DEBUG true

CMD flask run --host=0.0.0.0
