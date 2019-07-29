#!/bin/bash
# A wrapper around /entrypoint.sh to trap the SIGINT signal (Ctrl+C) and forwards it to the daemon
# In other words : traps SIGINT and SIGTERM signals and forwards them to the child process as SIGTERM signals

before() {
  ssh-agent -a /tmp/ssh-agent.socket
}

asyncRun() {
    "$@" &
    pid="$!"
    trap "echo 'Stopping PID $pid'; kill -SIGTERM $pid" SIGINT SIGTERM

    # A signal emitted while waiting will make the wait command return code > 128
    # Let's wrap it in a loop that doesn't end before the process is indeed stopped
    while kill -0 $pid > /dev/null 2>&1; do
	wait
    done
}

before

if [ "sleep" = "$1" ]; then
    # Interactive with trap
    asyncRun $@
else
    exec "$@"
fi
