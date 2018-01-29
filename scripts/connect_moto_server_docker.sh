## WEBAPP

# Step 1: Add a boto2 config file (smart_open uses boto2) to the container. Note the port and proxy host are dependent on what is in the docker-compose for the fake s3
docker exec webapp sh -c "echo '[Boto] \nis_secure = False \nhttps_validate_certificates = False \nproxy_port = 3000 \nproxy = s3' > /etc/boto.cfg"

# Step 2: Create our fake bucket in a kind of roundabout way: copy a file that runs Python code to the container, then run that file. This bucket name also must match up with what is specified in the docker-compose
docker cp scripts/connect_moto_server.sh webapp:/connect_moto_server.sh
docker exec webapp /bin/bash /connect_moto_server.sh

# Step 3: Touch a file to make Flask reload and pick up the boto proxy config. This will only work if Flask is in debug mode
docker exec webapp touch /csh/webapp/webapp/__init__.py


## MATCHER
# The matcher appears to use both boto2 and boto3. So we do the boto config change as in the webapp, but also set an environment variable (in the docker-compose) to cover boto3
docker exec matcher sh -c "echo '[Boto] \nis_secure = False \nhttps_validate_certificates = False \nproxy_port = 3000 \nproxy = s3' > /etc/boto.cfg"
docker exec matcher touch /csh/matcher/matcher/__init__.py
