# Flask app in order to help users track their blood pressure readings.
This repo uses my [Flask base repo](https://github.com/itprohelper/flask_base) which intends to make easier to setup a development using Docker.

## How to run this container?
Using your terminal go to the directory where you cloned this repo and then start the containers using [docker compose](https://docs.docker.com/compose/) I created this branch mainly for local testing. You need to get your Letsencrypt certs and create them locally.

```bash
docker compose up --build 
```
(re-run the above command every time you make a change.)

## Setup your environment variables
You will need to create a file .env under the www/ directory with the following values:

```bash
SECRET_KEY=<your_secret_key>
SQLALCHEMY_DATABASE_URI=sqlite:///site.db (this is an example-point your DB to the right location)
MAIL_SERVER=<your_SMTP_server>
MAIL_PORT=<port_your_mail_server_uses>
MAIL_USE_TLS=True or False
MAIL_USERNAME=<your_email_for_sending>
MAIL_PASSWORD=<your_mail_server_password>
```
## Things I need to fix/create
1. Create calendar view for blood preassure readings.
2. Allow users to email readings.
3. Migrate to MySQL/Postgres. What do you recommend for a simple database?

## Notes
I implemented the SSL using Letsencrypt. I pointed the certs location in the docker-compose yml file. It was tricky, but I did it. I tried to use the help of AI, but it wasn't really helpful. I eneded up looking for old notes and doing online searches.

## More details are coming soon.
I also write some brief tutorials on different subjects hoping to help somebody.
See them on my site [ITPro Helper](https://itprohelper.com)

## Special thanks for the great inspiration using Flask
[Miguel Grinberg](https://blog.miguelgrinberg.com)

[Corey Schafer](https://coreyms.com)

