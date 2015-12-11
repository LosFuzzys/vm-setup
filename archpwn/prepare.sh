#!/bin/bash

set -eux -o pipefail

USER=root
FILES_LOCATION="/tmp/install/"

function RUN() {
    sudo -H -u $USER "$@"
}

function USER() {
    USER=$1
}

function WORKDIR() {
    pushd $1
}

function ENV() {
    export $1=$2
}

function ADD() {
    cp "$FILES_LOCATION/$1" "$2"
}

function FROM() { echo "[-] Ignoring FROM"; }
function WORKDIR() { echo "[-] Ignoring WORKDIR"; }
function ENTRYPOINT() { echo "[-] Ignoring ENTRYPOINT"; }



source Dockerfile
