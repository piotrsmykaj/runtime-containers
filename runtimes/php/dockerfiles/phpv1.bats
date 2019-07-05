#!/usr/bin/env bats

@test "init_cphp_env" {
     [ "${CONTINUOUSPHP}" = "continuousphp" ]
     [ "${TERM}" = "xterm" ]
     [ "${WHITE}" = "\x1B033[0;02m" ]
     [ "${GREEN}" = "\x1B[1;32m" ]
     [ "${RED}" = "\x1B[1;31m" ]
     [ "${YELLOW}" = "\x1B[1;33m" ]
     [ "${BLUE}" = "\x1B[1;34m" ]
     [ "${PINK}" = "\x1B[1;35m" ]
     [ "${CYAN}" = "\x1B[1;36m" ]
     [ "${NORMAL}" = "\x1B[0;39m" ]
}

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
@test "ssh_login_fix" {

}
@test "setting_cphp_user" {
      [ $(getent group cphp) ]
      [ -f /etc/sudoers.d/cphp ]
      sh -c "id -u cphp"
      [ 0 -eq $? ]
      [ -d /home/cphp/var ]
      [ -f /usr/bin/git_ssh.sh ]
      [ -f /etc/profile.d/git-env.sh ]
      [ -f /etc/profile.d/ssh-agent.sh ]
      [ -f /etc/profile.d/continuousphp-env.sh ]
      [ -f /home/cphp/.ssh/authorized_keys ]
      [ -d /var/www ]
      [ -L /var/www/html ]
}
@test "bootstrap_cphp_env" {
      [ -f /tmp/bootstrap.sh ]
      [ -f /home/cphp/.profile ]
      sh -c /tmp/bootstrap.sh
      [ 0 -eq $? ]
}
@test "n" {
      
}
@test "pip_and_coid" {
      sh -c "dpkg-query -l python3-pip"
      [ 0 -eq $? ]
      sh -c "dpkg-query -l python3-dev"
      [ 0 -eq $? ]
      sh -c "pip3 show awscli"
      [ 0 -eq $? ]
}
@test "azure - command line" {
    [ "`su - cphp -c \"whereis azure\" | awk '{print $2}'`" = "/home/cphp/n/bin/azure" ]
}

@test "terraform" {

}