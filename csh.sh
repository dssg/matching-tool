#!/bin/bash

set -e -u

PROJECT="$(cat .project-name)"
PROJECT_HOME="$( cd "$( dirname "$0" )" && pwd )"
INFRASTRUCTURE_HOME="${PROJECT_HOME}"

cd $INFRASTRUCTURE_HOME

function help_menu () {
cat << EOF
Usage: ${0} {start|stop|build|rebuild|run|logs|status|destroy|all|}

OPTIONS:
   -h|help             Show this message
   start
   stop
   rebuild
   status
   destroy
   -t|triage
   -a|all

INFRASTRUCTURE:
   All the infrastructure needed is turned on!
        $ ./csh.sh start

   Check the status of the containers:
        $ ./csh.sh status

   Stop the csh's infrastructure:
        $ ./csh.sh stop

   Destroy all the resources related to the csh:
        $ ./csh.sh destroy

   Infrastructure logs:
        $ ./csh.sh -l

EOF
}

function start_infrastructure () {
    docker-compose --project-name ${PROJECT} up -d db webapp matcher worker redis
}

function stop_infrastructure () {
	docker-compose  --project-name ${PROJECT} stop
}

function build_images () {
	docker-compose  --project-name ${PROJECT} build "${@}"
}

function destroy () {
	docker-compose  --project-name ${PROJECT} down --rmi all --remove-orphans --volumes
}

function infrastructure_logs () {
    docker-compose --project-name ${PROJECT} logs -f -t
}

function status () {
	docker-compose --project-name ${PROJECT} ps
}


function debug () {
    docker exec -it "${1}" /bin/bash
}

function all () {
	build_images
	start_infrastructure
	status
}


if [[ $# -eq 0 ]] ; then
	help_menu
	exit 0
fi

case "$1" in
    start)
        start_infrastructure
		shift
        ;;
    stop)
        stop_infrastructure
		shift
        ;;
    build)
        build_images ${2}
		shift
        ;;
    rebuild)
        build_images --no-cache
		shift
        ;;
    -d|destroy)
        destroy
		shift
        ;;
    -l|logs)
        infrastructure_logs
		shift
        ;;
    status)
        status
		shift
	;;
    debug)
        debug ${2}
		shift
        ;;
   -a|--all)
       all
                shift
        ;;
    -h|--help)
        help_menu
                shift
        ;;
   *)
       echo "${1} is not a valid flag, try running: ${0} --help"
	   shift
       ;;
esac
shift

cd - > /dev/null
