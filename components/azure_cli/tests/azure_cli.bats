
@test "azure - command line" {
    [ "`su - cphp -c \"whereis azure\" | awk '{print $2}'`" = "/home/cphp/n/bin/azure" ]
}
