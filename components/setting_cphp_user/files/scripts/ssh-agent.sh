pgrep ssh-agent >/dev/null
if [[ $? -ne 0 ]] ; then
  if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval `ssh-agent -s` > /dev/null
    ssh-add > /dev/null
  fi
fi
