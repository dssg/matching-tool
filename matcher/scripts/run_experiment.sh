#!/bin/bash

set -e -u

# Name of the ec2 machines
NODE_NAME=csh-${USER}-

# Number of experiments to run
NUM_EXPERIMENTS=$(ls ../config/*.env | wc -l)

# We want machines in AWS
MACHINE_DRIVER=amazonec2

# EC2 instance type
AWS_INSTANCE_TYPE=t2.2xlarge


function help_menu () {
cat << EOF
Usage: ${0} {start|stop|build|rebuild|run|logs|status|destroy|all|}

OPTIONS:
   -h|help             Show this message
   install             Creates the ${NODE_NAME} machines in AWS
   run		       Runs the experiment
   stop		       Stops the ${NODE_NAME} machines in AWS
   start	       Starts the ${NODE_NAME} machines in AWS 
   destroy	       Destroy the ${NODE_NAME} machines in AWS
EOF
}

function setup_machines() {
    counter=1
    for experiment in ../config/*.env
    #for counter in $(seq 1 2)
    do
	 #echo "Creating machine ${NODE_NAME}${counter} for experiment ${experiment##*/}"
	 docker-machine create --driver ${MACHINE_DRIVER} --amazonec2-instance-type ${AWS_INSTANCE_TYPE} ${NODE_NAME}${counter}
	 docker-machine ssh ${NODE_NAME}${counter} sudo usermod -aG docker ubuntu
	 docker-machine scp install.sh ${NODE_NAME}${counter}:/home/ubuntu/install.sh
	 docker-machine scp run.sh ${NODE_NAME}${counter}:/home/ubuntu/run.sh 
	 docker-machine ssh ${NODE_NAME}${counter} chmod +x /home/ubuntu/install.sh
	 docker-machine ssh ${NODE_NAME}${counter} chmod +x /home/ubuntu/run.sh
	 docker-machine ssh ${NODE_NAME}${counter} /home/ubuntu/install.sh
	 echo "Copying the parameteres of the experiment"
	 docker-machine scp ${experiment} ${NODE_NAME}${counter}:/home/ubuntu/csh/matcher.env
	 let counter++
    done

}

function run_experiment() {
    for N in $(seq 1 $NUM_EXPERIMENTS)		      
    do
	docker-machine scp run.sh ${NODE_NAME}${N}:/home/ubuntu/run.sh
	docker-machine ssh ${NODE_NAME}${N} chmod +x /home/ubuntu/run.sh	
	docker-machine ssh ${NODE_NAME}${N} /home/ubuntu/run.sh
    done
}

function start_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	docker-machine start ${NODE_NAME}${N}
    done
}

function stop_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	docker-machine stop ${NODE_NAME}${N}
    done
}

function destroy_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	echo docker-machine rm -y ${NODE_NAME}${N}
    done
}



if [[ $# -eq 0 ]] ; then
	help_menu
	exit 0
fi

case "$1" in
    install)
	setup_machines
	shift
	;;
    run)
	run_experiment
	shift
	;;
    stop)
	stop_machines
	shift
	;;
    start)
	start_machines
	shift
	;;
    destroy)
	destroy_machines
	shift
	;;
    -h|help)
        help_menu
                shift
        ;;
   *)
       echo "${1} is not a valid flag, try running: ${0} --help"
	   shift
       ;;
esac
shift

    
