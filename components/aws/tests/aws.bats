@test "awscli" {
    aws --version
    [ 0 -eq $? ]

    pip list | grep awscli
    [ 0 -eq $? ]
}
