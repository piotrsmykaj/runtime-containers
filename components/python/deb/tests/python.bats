
@test "python3" {
      su - cphp -c "dpkg-query -l python3" 3>- &
      [ 0 -eq $? ]
}