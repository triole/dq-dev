#!/bin/bash

function clone() {
    url="${1}"
    fol="${2}"
    if [[ ! -d "${fol}" ]]; then
        echo "Clone ${url}"
        git clone "${url}" "${fol}"
    fi
}

function maybe_copy() {
    source_file="${1}"
    target_file="${2}"
    if [[ "${3}" == "sudo" ]]; then
        cmd="sudo cp -f"
    else
        cmd="cp -f"
    fi
    if [[ ! -f "${target_file}" ]]; then
        cmd="${cmd} \"${source_file}\" \"${target_file}\""
        echo "${cmd}"
        eval "${cmd}"
    fi
}

function get_container_ip() {
    hostname -I | awk '{print $1}'
}
