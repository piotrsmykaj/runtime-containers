#!/bin/bash

# First we need a ready build php-runtime instance stoped in AMI account

# 1. Package Test Activity will start ec2 if stopped.
# 2. Package Test Activity will copy tar.gz in EC2 with buildID directory
# 3. Test Generic Runtime X activity will ssh exec the build and test of specific runtime
# 4. Deploy Activity will ssh exec the docker tag and push of specific runtime

# IMPROVEMENT:
# Use hash on runtime to detect which need to be rebuild, avoiding rebuild of all runtimes
