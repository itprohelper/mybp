# A simple Flask app container.
FROM python:3.9-buster
LABEL maintainer="ITProHelper.com"

RUN apt-get update && apt-get -y install ntp 

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip install -r requirements.txt

# Set environment for flask
ENV FLASK_APP=run.py

# TODO como hacer para correr models.py y crear tables?
#RUN python3 \
#    && from mbp import db \
#    && db.create_all() \
#    && exit()

#CMD flask run
#RUN python createdb.py (ver ejemplo del Bret docker capitan para esperar que el DB empieze primero y despues correr esto)
CMD python run.py
