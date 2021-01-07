# A simple Flask app container.
FROM python:3-buster
LABEL maintainer="ITPro Helper"

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
#RUN python createdb.py
CMD python run.py



