# matching-tool
Integrating HMIS and criminal-justice data

## Requirements

- Docker and Docker-Compose; this is not strictly needed, but the only way to install that DSaPP is supporting and documenting.
- AWS S3; For development and testing purposes, [Moto standalone S3 server](#s3-credentials) can work, but it is not meant for production as the stored S3 data will disappear as soon as the process ends.


## Deploy with Docker

### Production

### NOTES
1. Set up a Postgres server. [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html) is recommended, though you may set up and administrate your own if desired.
2. Set up a machine/instance that will run the matching tool. Log into this machine; the rest of the steps assume that you are on the machine.
3. Clone the git repository: `git clone https://github.com/dssg/matching-tool.git` (this will require git to be installed if the machine didn't come with it)
4. `cd matching-tool` to change into the repository root directory.
5. Run the docker install script. Log out and back in when it completes. `./scripts/1_install_docker`
6. Run the database prepare script. This will create a Postgres database and populate the .env file needed to run the docker infrastructure. It requires the following arguments:
	- The address of the running Postgres server from step 1
	- The port of the running Postgres server from step 1
	- The name and password of a superuser on the Postgres server from step 1 that can create databases. If you are using Amazon RDS as directed, this user is created as part of the Postgres launch step.
	- The name of a new database to create for the webapp

	The script is run like this: `./scripts/2_prepare_db PGSERVER PGPORT SUPER_USER NEW_DATABASE`
	Example: `./scripts/2_prepare_db mypostgres.county.gov 5432 postgresadmin matching_tool`
	In addition to the Postgres database, this will prepopulate a .env file of environment variables that the Docker infrastructure will use.
7. Add AWS environment variables for S3 access:
	- Open up your .env file and modify the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables with your values. Visit [Managing Access Keys for your AWS Account](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) if you don't have an access key yet.
	- Open up the webapp.env file and modify all the instances of `your-bucket` to an S3 bucket you want to use to store data.
8. (optional) If you would like the web application to be able to send mail (e.g. for the reset password form), also modify the `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_DEFAULT_SENDER` variables. Depending on your mailing setup, `MAIL_PORT` (default: 465), `MAIL_USE_SSL` (default: True), `MAIL_USE_TLS` (default: False) can be overridden. If you don't set any mail environment variables, the reset password form will not work, but the rest of the app will.
9. (optional) Perform Redis tweaks. This is tested on Ubuntu. For other OSes, the method for making these changes may be different. Also, the need these changes may not be there for all OSes; Ubuntu's default configuration is not ideal for Redis within docker. If you're not sure, when you start up docker-compose in step 4, if Redis throws any warnings, listen to them. It will run without these, but without doing this you may increase the chances for weird system errors.
	- Disable Transparent HugePage in the current session: `echo never > /sys/kernel/mm/transparent_hugepage/enabled`
	- Disable Transparent HugePage for future reboots: modify the /etc/rc.local file as root
	- Enable overcommitt memory: `sudo sysctl vm.overcommit_memory=1`
10. Initialize the webapp database and create a web user with the `create_user` script. The script requires the following:
	- A short name for your jurisdiction (e.g. 'Cook'). Don't include spaces as it will confuse the script. This is just the name that shows up at the top of the webapp.
	- An email address for the web app login user
	- A password for the web app login user
	- A list of 'event types' that the user will have access to upload (e.g. `hmis_service_stays`, `jail_bookings`). If you want to see all the available event types, run the script without any to see the full list (e.g. `./scripts/3_create_user`)
	Example: `./scripts/3_create_user mycounty thcrockett@uchicago.edu password hmis_service_stays jail_bookings`
11. At this point, the web app should be running at port 80 on the machine.

### Development
1. Set up needed environment variables.
 - S3: Ideally, this should be run on an EC2 instance with an IAM role capable of accessing S3. You can totally ignore any S3 environment variables in that case. If not, ensure that you have values for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` set globally, or any other way that [boto3 can read](http://boto3.readthedocs.io/en/latest/guide/configuration.html).
 - Flask, Postgres: These are set up by the development docker-compose, so no need to do anything here.
2. Install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)
3. Bring up the docker containers using our development docker-compose: `docker-compose up`
4. Initialize the database and users. You can use this script to get set up easily, including a user 'testuser@example.com' with password 'password', that you can use to log in: `sh scripts/create_test_users_docker.sh`

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
