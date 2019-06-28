#!/usr/bin/env bats

@test "Node installed in user CPHP" {
    su - cphp -c "node --version"
    [ 0 -eq $? ]

    su - cphp -c "npm --version"
    [ 0 -eq $? ]
}

@test "azure - command line" {
    [ "`su - cphp -c \"whereis azure\" | awk '{print $2}'`" = "/home/cphp/n/bin/azure" ]
}
