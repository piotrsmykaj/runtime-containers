
@test "setting_cphp_user" {
      [ $(getent group cphp) ]
      [ -f /etc/sudoers.d/cphp ]
      id -u cphp
      [ 0 -eq $? ]
      [ -d /home/cphp/var ]
      [ -f /etc/profile.d/ssh-agent.sh ]
      [ -f /etc/profile.d/continuousphp-env.sh ]
      [ -d /var/www ]
      [ -L /var/www/html ]
}
