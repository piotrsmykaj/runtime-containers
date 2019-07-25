
@test "terraform" {
      su - cphp -c "terraform --version" 3>- &
      [ 0 -eq $? ]
}

