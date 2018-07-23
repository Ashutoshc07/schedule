#!/bin/bash
IFACE=$1
IFACE=${IFACE:-eth1.610}
CONTAINER=$(docker run -d --net="none" --privileged=true twin_peaks/tp-ubuntu-ped-docker /bin/sh -c "while true; do echo hello world; sleep 1; done")
sudo /usr/local/bin/pipework ${IFACE} -i eth0 ${CONTAINER} 0/0
docker exec -it ${CONTAINER} bash
docker stop ${CONTAINER}
docker rm -f ${CONTAINER}
