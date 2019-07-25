#!/bin/bash

if [[ $(docker images -q $1) == "" ]]; then
    exit 1
else
    exit 0
fi
