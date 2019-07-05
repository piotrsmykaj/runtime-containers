
@test "Node installed in user CPHP" {
    su - cphp -c "node --version"
    [ 0 -eq $? ]

    su - cphp -c "npm --version"
    [ 0 -eq $? ]
}
