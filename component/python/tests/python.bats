#!/usr/bin/env bats

@test "Python" {
    python --version
    [ 0 -eq $? ]
}

@test "Pip - Python packager" {
    [ "`pip --version | awk '{ print $1 }'`" = "pip" ]
}
