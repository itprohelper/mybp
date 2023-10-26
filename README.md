# Flask app in order to help users track their blood pressure readings.
This repo uses my [Flask base repo](https://github.com/itprohelper/flask_base) which intends to make easier to setup a development using Docker.

## How to run this container?
Using your terminal go to the directory where you cloned this repo and then start the containers using [docker compose](https://docs.docker.com/compose/)

```bash
docker compose up
```
## Setup your environment variables
You will need to create a file .env under the www/ directory with the following values:

```bash
SECRET_KEY=<your_secret_key>
SQLALCHEMY_DATABASE_URI=sqlite:///site.db (this is an example-poing your DB to the right location)
MAIL_SERVER=<your_SMTP_server>
MAIL_PORT=<port_your_mail_server_uses>
MAIL_USE_TLS=True or False
MAIL_USERNAME=<your_email_for_sending>
MAIL_PASSWORD=<your_mail_server_password>
```

## To be done
I need help implementing a SSL cert using Docker compose in production. I tried using the docker image from certbot/certbot:latest, but 
it is taking me too long to implement it. Yes, I'm using google to search for options. If anybody has done it please share some ideas if you like. I'm still learning. Thanks.

## More details are coming soon.
I also wrote some brief tutorials on different subjects hoping to help somebody.
See them on my site [ITPro Helper](https://itprohelper.com)
