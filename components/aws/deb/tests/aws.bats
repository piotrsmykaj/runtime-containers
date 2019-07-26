@test "aws" {
      pip3 show awscli
      [ 0 -eq $? ]
}