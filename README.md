# matching-tool
Integrating HMIS and criminal-justice data

## Requirements

- Docker and Docker-Compose; this is not strictly needed, but the only way to install that DSaPP is supporting and documenting.
- AWS S3; For development and testing purposes, [Moto standalone S3 server](#s3-credentials) can work, but it is not meant for production as the stored S3 data will disappear as soon as the process ends.


## Deploy with Docker

### Development
1. Set up needed environment variables.
 - S3: Ideally, this should be run on an EC2 instance with an IAM role capable of accessing S3. You can totally ignore any S3 environment variables in that case. If not, ensure that you have values for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` set globally, or any other way that [boto3 can read](http://boto3.readthedocs.io/en/latest/guide/configuration.html).
 - Flask, Postgres: These are set up by the development docker-compose, so no need to do anything here.
2. Install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)
3. Bring up the docker containers using our development docker-compose: `docker-compose up`
4. Initialize the database and users. You can use this script to get set up easily, including a user 'testuser@example.com' with password 'password', that you can use to log in: `sh scripts/create_test_users_docker.sh`

### Production

1. Set up needed environment variables.
 - S3: Ideally, this should be run on an EC2 instance with an IAM role capable of accessing S3. You can totally ignore any S3 environment variables in that case. If not, ensure that you have values for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` set globally, or any other way that [boto3 can read](http://boto3.readthedocs.io/en/latest/guide/configuration.html).
 - Flask: `SECRET_KEY` and `SECURITY_PASSWORD_SALT` can be any strings you'd like, but keep them secret! Set `DEBUG` to False
 - Postgres: docker-compose will use `PGPASSWORD`, `PGDATABASE`, and `PGUSER` to both set up a database and pass them to the applications to connect. Since docker-compose handles the whole thing, they can be any arbitrary strings, but again keep them secret.
 - Mail: `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_DEFAULT_SENDER` are needed to configure transactional email (like the reset password functionality). Depending on your mailing setup, `MAIL_PORT` (default: 465), `MAIL_USE_SSL` (default: True), `MAIL_USE_TLS` (default: False) can be overridden. If you don't set any mail environment variables, the reset password form will not work, but the rest of the app will.

2. Install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)
3. Perform Redis tweaks. This is tested on Ubuntu. For other OSes, the method for making these changes may be different. Also, the need these changes may not be there for all OSes; Ubuntu's default configuration is not ideal for Redis within docker. If you're not sure, when you start up docker-compose in step 4, if Redis throws any warnings, listen to them. It will run without these, but without doing this you may increase the chances for weird system errors.
	- Disable Transparent HugePage in the current session: `echo never > /sys/kernel/mm/transparent_hugepage/enabled`
	- Disable Transparent HugePage for future reboots: modify the /etc/rc.local file as root
	- Enable overcommitt memory: `sudo sysctl vm.overcommit_memory=1`
4. Bring up the docker containers, with our production docker-compose: `docker-compose -f docker-compose-prod.yml up`
5. Initialize the database and users. You'll want to be more deliberate about this than in Development mode, so instead of running the test users script we'll go through the steps one by one:
	- Initialize the database: `docker exec -it webapp alembic upgrade head`
	- Create a user. Change the password from this example for sure, and change the email address to the real email address of the user: `docker exec -it webapp flask users create --password password -a testuser@example.com`
	- Create one or more roles, given a short name for your jurisdiction (the name you choose should not include underscores), and an event type corresponding to the type of data you want to upload. Here's an example for Cook county and 'hmis_service_stays': `docker exec -it webapp flask roles create cook_hmis_service_stays`. Full list of available schemas:
		- `by_name_list`
		- `case_charges`
		- `hmis_aliases`
		- `hmis_service_stays`
		- `jail_bookings`
		- `jail_booking_aliases`
		- `jail_booking_charges`
	- Add your user to that role. Example using the user and role from above: `docker exec -it webapp flask roles add testuser@example.com cook_hmis_service_stays`

## Expunging Data

There is a data expunging script that is provided. It does *not* expunge individual records, but rather all records for a given jurisdiction and event type, both from S3 and the database. It exists as a Flask CLI command in the webapp container. It prompts you for confirmation before doing so.

- Get a docker shell: `docker exec -it webapp /bin/bash`
- `flask expunge test jail_bookings` (in this example, 'test' is the jurisdiction and 'jail_bookings' is the event type)


## Browser Support
The web app is tested on the following browsers:

- Firefox 52 and above
- Chrome 61
- IE 11

If you test with any other browsers, add them to this list!


## S3 Credentials
This project utilizes [smart_open](https://github.com/RaRe-Technologies/smart_open) for S3 connectivity, which itself uses [Boto 2](http://boto.cloudhackers.com/en/latest/). Credentials are handled at the Boto level, so you may utilize either environment variables or Boto config files to pass credentials to the application.

See more details at the [Boto Docs](http://boto.cloudhackers.com/en/latest/boto_config_tut.html)

For development, we recommend using moto's [standalone server mode](https://github.com/spulec/moto#stand-alone-server-mode). The server is in requirements_dev already, so here's a quick guide without changing any code:

1. Create a `~/.boto` file with:

```
[Boto]
is_secure = False
https_validate_certificates = False
proxy_port = 3000
proxy = 127.0.0.1

[Credentials]
aws_access_key_id = fake
aws_secret_access_key = fake
```
2. `moto_server s3 -p3000`
3. Create the bucket specified in your docker-compose file. You will have to do this each time you start the fake server. The example has 'your-bucket', so for instance you can run this in a python console:

```
import boto
conn = boto.connect_s3()
conn.create_bucket('your-bucket')
```

## Acceptance Testing

This repository has acceptance tests written using Nightwatch, which comes bundled in our JS developer dependencies so you don't need to install it separately. However, requires a locally running Selenium server and the Chrome driver. Later we will add other browsers to this setup.

- [Download the Selenium standalone server](http://www.seleniumhq.org/download/)
- [Download the ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

To make the ChromeDriver executable work with our nightwatch config, it needs to be available in your PATH.

The Selenium server is packaged as a JAR file, so you can run it as any other JAR file: `java -jar <path/to/selenium/jar/file>`

The acceptance tests rely on some test users and jurisdictions in the webapp's database. This is covered in the setup at the top of this README, so make sure that is completed before trying to run these tests.

You can run the tests by navigating to the `webapp/frontend` directory and running `npm run acceptance`. If all goes well, you should see many instances of Chrome pop up, a bunch of text entry, clicking and page loading, and all tests passing in your console.

## Further Details
The subprojects for the [matching service](matcher) and [web application](webapp) have READMEs that talk more about details specific to those subprojects
