# Installing the matching-tool

## Requirements

- Docker and Docker-Compose; this is not strictly needed, but the only way to install that DSaPP is supporting and documenting.
- We strongly recommend running on a Linux machine and particularly recommend Ubuntu as some of the installation convenience scripts do assume Ubuntu. If this is being run on an Amazon Web Services instance, a well-tested choice is community AMI id `ami-79873901`. If being run locally, run Ubuntu Xenial 16.04 Server Edition.
- AWS S3 by default, or enough space on the local filesystem to handle uploaded files.


## Deploy with Docker

If you are deploying the matching tool with the goal of having users actively use it to upload real data, and you want that data to persist, follow the [Production](#production) section. If you just want to try out the tool with fake data and do active development on it, follow the [Developer](/dev/getting-started) section.

1. Set up a Postgres server. [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html) is recommended, though you may set up and administrate your own if desired.
2. Set up a machine/instance that will run the matching tool (see [requirements](#requirements) section for recommendations). Log into this machine; the rest of the steps assume that you are on the machine.
3. Clone the git repository: `git clone https://github.com/dssg/matching-tool.git` (this will require git to be installed if the machine didn't come with it)
4. `cd matching-tool` to change into the repository root directory.
5. Install docker and docker-compose. If you are on an Ubuntu machine, you can use the included executable script `./scripts/1_install_docker` as a convenience for doing so. Otherwise, refer to the [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install/) documentation. If running the included install script, log out and back in when it completes as it will add your user to the 'docker' group, and that change requires a new login to take effect.
6. Run the database prepare script. This will create a Postgres database and populate the .env file needed to run the docker infrastructure. It requires the following arguments:
	- The address of the running Postgres server from step 1
	- The port of the running Postgres server from step 1
	- The name and password of a superuser on the Postgres server from step 1 that can create databases. If you are using Amazon RDS as directed, this user is created as part of the Postgres launch step.
	- The name of a new database to create for the webapp

	The script is run like this: `./scripts/2_prepare_db PGSERVER PGPORT SUPER_USER NEW_DATABASE`
	Example: `./scripts/2_prepare_db mypostgres.county.gov 5432 postgresadmin matching_tool`
	In addition to the Postgres database, this will prepopulate a .env file of environment variables that the Docker infrastructure will use.

7. Set up storage.
    1. Option 1 (S3):
	    - Open up your .env file and modify the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables with your values. Visit [Managing Access Keys for your AWS Account](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) if you don't have an access key yet.
	    - Open up the webapp.env file and modify all the instances of `your-bucket` to an S3 bucket you want to use to store data.
    2. Option 2 (Filesystem): [configuration changes](install.md#using-the-filesystem)
8. (optional) If you would like the web application to be able to send mail (e.g. for the reset password form), also modify the `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_DEFAULT_SENDER` variables. Depending on your mailing setup, `MAIL_PORT` (default: 465), `MAIL_USE_SSL` (default: True), `MAIL_USE_TLS` (default: False) can be overridden. If you don't set any mail environment variables, the reset password form will not work, but the rest of the app will.
9. (optional) Perform Redis tweaks. This is tested on Ubuntu. For other OSes, the method for making these changes may be different. Also, the need these changes may not be there for all OSes; Ubuntu's default configuration is not ideal for Redis within docker. If you're not sure, when you start up docker-compose in step 4, if Redis throws any warnings, listen to them. It will run without these, but without doing this you may increase the chances for weird system errors.
	- Disable Transparent HugePage in the current session: `echo never > /sys/kernel/mm/transparent_hugepage/enabled`
	- Disable Transparent HugePage for future reboots: modify the /etc/rc.local file as root
	- Enable overcommit memory: `sudo sysctl vm.overcommit_memory=1`
10. Initialize the webapp database and create a web user with the `create_user` script. The script requires the following:
	- A short name for your jurisdiction (e.g. 'Cook'). Don't include spaces as it will confuse the script. This is just the name that shows up at the top of the webapp.
	- An email address for the web app login user
	- A password for the web app login user
	- A list of 'event types' that the user will have access to upload (e.g. `hmis_service_stays`, `jail_bookings`). If you want to see all the available event types, run the script without any to see the full list (e.g. `./scripts/3_create_user`)
	- Example: `./scripts/3_create_user mycounty thcrockett@uchicago.edu password hmis_service_stays jail_bookings`
11. At this point, the web app should be running at port 80 on the machine.

## Using the Filesystem

The code in both the webapp and the matching service support both S3 and filesystem schemes for storage. However, since they need to communicate data between each other, and by default they are in separate Docker containers with separate filesystems, to use the filesystem you must also modify the docker-compose.yml to mount a shared volume from the host machine between the `webapp`, `webapp_worker`, and `matcher_worker` containers.

For instance: `mkdir ./shared-volume; chmod 777 ./shared-volume` would then allow you to add the following volume to each of those containers:

`- ./shared-volume:/shared-volume`

With this in place, each container will have a `/shared-volume` directory that can be used as a root directory for the various `_PATH` variables in `webapp.env`
