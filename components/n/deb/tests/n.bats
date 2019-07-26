
@test "n" {
    su - cphp -c "node --version" 3>- &
    [ 0 -eq $? ]

}