
@test "azure - command line" {
    az=$(su - cphp -c "whereis azure" 3>- &)
    result=$(echo ${az} | awk '{print $2}')
    [ ${result} = "/home/cphp/n/bin/azure" ]
}
