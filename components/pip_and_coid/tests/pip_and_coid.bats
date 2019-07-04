#!/usr/bin/env bats

@test "pip_and_coid" {
      sh -c "dpkg-query -l python3-pip"
      [ 0 -eq $? ]
      sh -c "dpkg-query -l python3-dev"
      [ 0 -eq $? ]
      sh -c "pip3 show awscli"
      [ 0 -eq $? ]
}