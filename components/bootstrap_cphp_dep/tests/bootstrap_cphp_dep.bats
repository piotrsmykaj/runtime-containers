#!/usr/bin/env bats

@test "bootstrap_cphp_env" {
      [ -f /tmp/bootstrap.sh ]
      [ -f /home/cphp/.profile ]
      sh -c /tmp/bootstrap.sh
      [ 0 -eq $? ]
}