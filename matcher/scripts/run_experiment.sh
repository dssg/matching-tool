#!/bin/bash

set -e -u

# Name of the ec2 machines
NODE_NAME=csh-${USER}-

# Number of experiments to run
NUM_EXPERIMENTS=$(ls ../config/*.env | wc -l)


function help_menu () {
cat << EOF
Usage: ${0} {start|stop|build|rebuild|run|logs|status|destroy|all|}

OPTIONS:
   -h|help             Show this message
   setup               Creates the ${NODE_NAME} EC2 machines in AWS and configures them
   run		       Runs the experiment
   stop		       Stops the ${NODE_NAME} machines in AWS
   start	       Starts the ${NODE_NAME} machines in AWS 
   destroy	       Destroy the ${NODE_NAME} machines in AWS
EOF
}

function setup_machine() {
    counter=$1

    # Name of the ec2 machines
    NODE_NAME=csh-${USER}-
    
    # We want machines in AWS
    MACHINE_DRIVER=amazonec2

    # EC2 instance type
    AWS_INSTANCE_TYPE=t2.micro

    echo "Creating machine ${NODE_NAME}${counter} using ${AWS_INSTANCE_TYPE}"
    docker-machine create --driver ${MACHINE_DRIVER} --amazonec2-instance-type ${AWS_INSTANCE_TYPE} ${NODE_NAME}${counter}
    docker-machine ssh ${NODE_NAME}${counter} sudo usermod -aG docker ubuntu
    docker-machine scp install.sh ${NODE_NAME}${counter}:/home/ubuntu/install.sh
    docker-machine scp run.sh ${NODE_NAME}${counter}:/home/ubuntu/run.sh 
    docker-machine ssh ${NODE_NAME}${counter} chmod +x /home/ubuntu/install.sh
    docker-machine ssh ${NODE_NAME}${counter} chmod +x /home/ubuntu/run.sh
    docker-machine ssh ${NODE_NAME}${counter} /home/ubuntu/install.sh
    echo "Copying the parameteres of the experiment"
    docker-machine scp ${experiment} ${NODE_NAME}${counter}:/home/ubuntu/csh/matcher.env
    docker-machine scp ../../.env ${NODE_NAME}${counter}:/home/ubuntu/csh/.env
}


export -f setup_machine

function setup_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	sem --bg -j $NUM_CORES setup_machine $N
    done
}

function run_experiment() {
    IP=$1
    JURISDICTION=$2
    EVENT_TYPE=$3
    UPLOAD_ID=$4

    echo http ${IP}/match/${JURISDICTION}/${EVENT_TYPE} uploadId==${UPLOAD_ID}
}

export -f run_experiment

function run_experiments() {
    IPS=$(docker-machine ls | sed '1d' | awk '{print $5}' | awk -F/ '{print $3}' | awk -F: '{print $1}')
    
    for ip in $IPS
    do
	sem --bg -j $NUM_CORES run_experiment $ip "${@}"
    done
}



function start_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	sem --bg -j $NUM_CORES docker-machine start ${NODE_NAME}${N}
    done
}

function stop_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	sem --bg -j $NUM_CORES docker-machine stop ${NODE_NAME}${N}
    done
}

function destroy_machines() {
    for N in $(seq 1 $NUM_EXPERIMENTS)
    do
	sem --bg -j $NUM_CORES docker-machine rm -y ${NODE_NAME}${N}
    done
}



if [[ $# -eq 0 ]] ; then
	help_menu
	exit 0
fi

case "$1" in
    setup)
	setup_machines
	shift
	;;
    run)
	run_experiments ${@:2}
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
