#!/bin/bash

# First we need a ready build php-runtime instance stoped in AMI account

# 1. Package Test Activity will start ec2 if stopped.
# 2. Package Test Activity will copy tar.gz in EC2 with buildID directory
# 3. Test Generic Runtime X activity will ssh exec the build and test of specific runtime
# 4. Deploy Activity will ssh exec the docker tag and push of specific runtime

# IMPROVEMENT:
# Use hash on runtime to detect which need to be rebuild, avoiding rebuild of all runtimes

# Export Variable Needed
# AWS_RUNTIME_EC2_ID

start_builder() {
  echo "Start ec2 $AWS_RUNTIME_EC2_ID..."
  ip="None"

  for (( ; ; ))
  do
    state=$(aws --profile runtime-containers-builder ec2 describe-instances --instance-ids $AWS_RUNTIME_EC2_ID --query "Reservations[0].[Instances][0][0].[State][0].[Name]" --output text)
    if [ "running" == "$state" ];
    then
      ip=$(aws --profile runtime-containers-builder ec2 describe-instances --instance-ids $AWS_RUNTIME_EC2_ID --query "Reservations[0].[Instances][0][0].PublicIpAddress" --output text)
      export EC2_IP=$ip
      echo "EC2 Runtime Builder IP: $ip"
      break
    fi

    aws ec2 start-instances --instance-ids $AWS_RUNTIME_EC2_ID
    sleep 20
  done
}

exec_builder() {
  ssh -t -i $AWS_SSH_KEY ec2-user@$EC2_IP "$1"
  return $?
}

run_copy_build_package() {
  echo "Copy package to EC2..."
  rm -rf .git
  tar czf /tmp/build.tar.gz .
  exec_builder "mkdir /usr/local/runtime-containers/$CPHP_BUILD_ID"
  scp -i $AWS_SSH_KEY /tmp/build.tar.gz ec2-user@$EC2_IP:/usr/local/runtime-containers/$CPHP_BUILD_ID || exit 1
  exec_builder "cd /usr/local/runtime-containers/$CPHP_BUILD_ID; tar xzf build.tar.gz" || exit 1
}

run_build() {
  runtime=$1
  version=$2
  exec_builder "cd /usr/local/runtime-containers/$CPHP_BUILD_ID; ./bin/docker-template build --runtime $runtime --version $version --verbose --replace" || return 1
  return 0
}

run_test() {
  runtime=$1
  version=$2
  pip3 install ansible
  exec_builder "cd /usr/local/runtime-containers/$CPHP_BUILD_ID && ./bin/docker-template test --runtime $runtime --version $version --verbose" || return 1
  return 0
}

run_deploy() {
  runtime=$1
  version=$2
  exec_builder "docker tag continuous:php_$version 310957825501.dkr.ecr.us-east-1.amazonaws.com/cphp/runtime/php:$version"
  exec_builder "aws ecr get-login --region us-east-1 --registry-ids 310957825501 --no-include-email | bash"
  exec_builder "docker push 310957825501.dkr.ecr.us-east-1.amazonaws.com/cphp/runtime/php:$version"
}

action=$1
runtime=$2
version=$3

start_builder

if [ "build" == "$action" ];
then
  run_build $runtime $version
  if [ 0 -eq $? ];
  then
    exit 0
  else
    exit 1
  fi
fi

if [ "test" == "$action" ];
then
  run_test $runtime $version
  if [ 0 -eq $? ];
  then
    exit 0
  else
    exit 1
  fi
fi

if [ "deploy" == "$action" ];
then
  run_deploy $runtime $version
  exit 0
fi

if [ "copy_build_package" == "$action" ];
then
  run_copy_build_package
  exit 0
fi


