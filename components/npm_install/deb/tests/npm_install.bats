
@test "npm installation" {
    su - cphp -c "npm --version" 3>- &
    [ 0 -eq $? ]
}
