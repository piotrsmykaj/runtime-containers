#!/usr/bin/env bats

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