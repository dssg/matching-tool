# Getting Started 

To make any changes to the matching tool, first you have to get the tool running on a computer.

1. Clone the git repository: `git clone https://github.com/dssg/matching-tool.git` (this will require git to be installed if the machine didn't come with it)
2. `cd matching-tool` to change into the repository root directory.
3. Install docker and docker-compose. If you are on an Ubuntu machine, you can use the included executable script `./scripts/1_install_docker` script as a convenience for doing so. Otherwise, refer to the [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install/) documentation. If running the included install script, log out and back in when it completes as it will add your user to the 'docker' group, and that change requires a new login to take effect.
4. Set up storage.
    1. Option 1 (S3):
	    - Open up your .env file and modify the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables with your values. Visit [Managing Access Keys for your AWS Account](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) if you don't have an access key yet.
	    - Open up the webapp.env file and modify all the instances of `your-bucket` to an S3 bucket you want to use to store data.
    2. Option 2 (Filesystem): [configuration changes](/admin/install.md#using-the-filesystem)
5. Bring up the docker containers using our development docker-compose: `docker-compose -f docker-compose-dev.yml up`
6. Initialize the database and users. You can use [this script](https://github.com/dssg/matching-tool/blob/master/scripts/development/create_test_users_docker.sh) to get set up easily, including a user `testuser@example.com` with password `password`, that you can use to log in: `sh scripts/development/create_test_users_docker.sh`
7. At this point, the web app should be running at port 80 on the machine.

At this point, you can proceed to the following pages, which cover common types of changes that developers may want to make to the tool.
