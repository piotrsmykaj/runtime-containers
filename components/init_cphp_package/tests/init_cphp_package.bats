#!/usr/bin/env bats


@test "init_cphp_package" {
    sh -c "dpkg-query -l apt-utils"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l ca-certificates"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l rpm"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l zip"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l unzip"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l curl"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l vim"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l git"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l build-essential"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l sudo"
    [ 0 -eq $? ]
    sh -c "dpkg-query -l openssh-server"
    [ 0 -eq $? ]
    [ -f /etc/dpkg/dpkg.cfg.d/01_nodoc ]
    [ -d /var/run/sshd ]
}