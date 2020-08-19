#!/bin/bash

IFS=$'\n'

ifil="${1}"
ofil="${2}"
tfil="$(tempfile)"

if [[ -z "${outfil}" ]]; then
    outfil="/dev/stdout"
fi

cp -f "${ifil}" "${tfil}"

for line in $(env | sort); do
    key=$(echo "${line}" | grep -Po "^[A-Z0-9-_]+")
    val=$(echo "${line}" | grep -Po "[^=]+$")
    if [[ (-n "${key}" && -n "${val}") ]]; then
        sed -i "s|<${key}>|${val}|g" "${tfil}"
    fi
done

cp -f "${tfil}" "${ofil}"
