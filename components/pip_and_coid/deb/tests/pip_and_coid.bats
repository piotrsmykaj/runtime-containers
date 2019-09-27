
@test "pip_and_coid" {
      dpkg-query -l python3-pip
      [ 0 -eq $? ]
      dpkg-query -l python3-dev
      [ 0 -eq $? ]
      pip --version
      [ 0 -eq $? ]
      pip3 --version
      [ 0 -eq $? ]
}
