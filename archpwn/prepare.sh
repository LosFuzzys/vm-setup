#!/bin/bash

set -eux -o pipefail

USER=root
FILES_LOCATION="/tmp/install/"

function RUN() {
    sudo -E -H -n -u "$USER" "$@"
}

function USER() {
    USER=$1
}

function WORKDIR() {
    pushd $1 || true
}

function ENV() {
    export $1=$2
}

function ADD() {
    cp "$FILES_LOCATION/$1" "$2"
    chown -R "$USER" "$2"
}

function CMD() {
    echo "[-] Warning: ingnoring CMD $@"
}

function FROM() { echo "[-] Ignoring FROM"; }
function ENTRYPOINT() { echo "[-] Ignoring ENTRYPOINT"; }
function VOLUME() { echo "[-] Ignoring VOLUME"; }

# source the docker file
source Dockerfile
