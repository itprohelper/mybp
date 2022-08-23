# A simple Flask app container.
FROM python:3.9-buster
LABEL maintainer="ITProHelper.com"

#Set the working directory
WORKDIR /opt/www

COPY requirements.txt requirements.txt

#Set environment for flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

#run some updates and install NTP server(need to see if I need this.)
RUN apt-get update

#Install requirements
RUN pip install -r requirements.txt

# Place app in container.
COPY . .

# Server port for  flask app
EXPOSE 5000

# TODO como hacer para correr models.py y crear tables?
#RUN python3 \
#    && from mbp import db \
#    && db.create_all() \
#    && exit()

CMD ["flask",  "run"]
#RUN python createdb.py habria que instalar mariadb client o correr esto en el Dockerfile en db.
#(ver ejemplo del Bret docker capitan para esperar que el DB empieze primero y despues correr esto)
#CMD python app.py