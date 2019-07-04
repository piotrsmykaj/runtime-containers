#!/usr/bin/env bats

@test "python3" {
      su - cphp -c "dpkg-query -l python3"
      [ 0 -eq $? ]
}