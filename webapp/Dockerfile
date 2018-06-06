FROM python:3.6.2

RUN apt-get -y update && \
	apt-get install unzip sudo

RUN mkdir -p /csh/webapp

# Prepare for React 
WORKDIR /csh/webapp/frontend
ADD . /csh/webapp/
RUN curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash - && \
    apt-get install -y nodejs && \
    npm cache clean -f && \
    npm install  -g n && \
    n stable && \
    npm install npm@latest -g && \
    npm install

# Prepare for flask 
WORKDIR /csh/webapp
ADD requirements.txt /csh/webapp/requirements.txt
ADD requirements_dev.txt /csh/webapp/requirements_dev.txt
ADD README.md /csh/webapp/README.md

RUN pip install -r requirements.txt

ADD setup.py /csh/webapp/setup.py

# Build frontend output.js
WORKDIR /csh/webapp/frontend
RUN npm run build && ls -alF /csh/webapp/webapp/static 

# Run flask app
WORKDIR /csh/webapp
ENV PYTHONPATH /csh/webapp
ENV FLASK_APP webapp.app
ENV FLASK_DEBUG true

CMD flask run --host=0.0.0.0
