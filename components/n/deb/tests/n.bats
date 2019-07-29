@test "n" {
    su - cphp -c "n ls"
    [ 0 -eq $? ]
    su - cphp -c "node --version"
    [ 0 -eq $? ]
    su - cphp -c "npm --version"
    [ 0 -eq $? ]
}
