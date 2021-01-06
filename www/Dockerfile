# A simple Flask app container.
FROM python:3-buster
LABEL maintainer="ITPro Helper"

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip install -r requirements.txt

# Run python interpreter > from mbp import db > db.create_all()
#RUN python createdb.py NO funciona aqui pero SI despues del build y up -d
#Need to find a way to run this after the container is UP.

CMD python run.py
