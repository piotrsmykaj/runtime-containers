#!/bin/sh
exec /usr/bin/ssh -o UserKnownHostsFile=/dev/null -o LogLevel=quiet -o StrictHostKeyChecking=no -i /home/cphp/.ssh/id_rsa "$@"
