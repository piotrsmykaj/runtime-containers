<a href="http://continuous.lu">
  <img src="https://app.continuousphp.com/assets/logos/continuousphp.svg" alt="ContinuousPHP" width="250px" align="right"/>
</a>

<p align="left">
  <a href="https://continuousphp.com/git-hub/continuousphp/runtime-containers"><img alt="Build Status" src="https://status.continuousphp.com/git-hub/continuousphp/cli?token=8eb1b41e-343a-41b5-b68f-179fb1ce1ffe&branch=master" /></a>
</p>

<p align="left">
    ContinuousPHP© is the first and only PHP-centric PaaS to build, package, test and deploy applications in the same workflow.
</p>

# Runtime Container

This repository will define the construction of all the runtime containers for ContinuousPHP CI/CD platform

Architecture:

  1. Components:
      Component are a *Docker template* shared playbook, it can be implemented inside a Runtime platform and have its own test write with `bats`.
      The implementation of the component is made using the docker template script in python.

  2. Runtimes:
      Runtime represents a platform around the same application goal (Language) like `php`, `javascript`, `ruby`, `python`.

  3. Flavours:
      A Flavour represent a docker image distribution like debian, alpine, centos...
      A Component will integrate a dedicated script for each flavour.

## Component

 - files
 - flavours
   - component.dtc
   - tests

### Docker Template Component

Docker Template Component have `.dtc` extension and are a template file that will define `Dockerfile` instructions dedicated of the current component.
Each flavours have dedicated `.dtc` file

The template must have the following functionality:
- [x] File path replacement ( replacement of the file path by the build context )
- [ ] Conditional statement of a runtime variable ( when runtime are build, I want condition the integration of the statement if variable condition are meet, like version of runtime php-7.1)

#### Additional files

When ADD or COPY are used in components, the specified must be stored inside a "files" directory but the written path must
follow the syntax: files/component_name/path_to_files_in_files_directory

## Runtime

### Runtime Configuration

The configuration must have the following functionality:
1. variable version for `FROM` instruction
2. flavours parsing to know witch flavour of components must be included
3. list of components to includes

## Getting Started

In order to use the binary `bin/docker-template`.
You have to install theses python dependencies:
*At least python 3.8 is required*

```bash
sudo yum install libssl-dev openssl
wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz
tar xzvf Python-3.8.1.tgz
cd Python-3.8.1
./configure
make
sudo make install
```

```
❯ pip3 install pyyaml
❯ ./bin/docker-template --help                                                                                                                          runtime-containers/git/feature/default_ssh_agent !+
usage: docker-template [-h] [--runtime [RUNTIME]]
                       [--version [VERSION [VERSION ...]]] [--clean]
                       [--verbose] [--replace]
                       [{build,test}]

Continuous runtime container generator

positional arguments:
  {build,test}          Command

optional arguments:
  -h, --help            show this help message and exit
  --runtime [RUNTIME]   Runtime
  --version [VERSION [VERSION ...]]
                        List of versions to compile
  --clean               Remove all temporary files
  --verbose             Print the entire output
  --replace             Rebuild existing images
```

### Build Runtime

```
❯ ./bin/docker-template build --runtime php --version 7.3.8-fpm --verbose
Step 8/8 : CMD [ "bats", "test.bats" ]
 ---> Running in 43ecc0b370b5
Removing intermediate container 43ecc0b370b5
 ---> b4d43d928f3c
Successfully built b4d43d928f3c
Successfully tagged bats_tests:latest
 Results of bats tests for version : 7.3.8-fpm
 
SSH_AUTH_SOCK=/tmp/ssh-agent.socket; export SSH_AUTH_SOCK;
SSH_AGENT_PID=7; export SSH_AGENT_PID;
echo Agent pid 7;
 ✓ init_cphp_env
 ✓ init_cphp_package
 ✓ ssh_login_fix
 ✓ setting_cphp_user
 ✓ bootstrap_cphp_env
 ✓ n
 ✓ pip_and_coid
 ✓ aws
 ✓ azure - command line
 ✓ terraform
 ✓ entrypoint

11 tests, 0 failures

Untagged: bats_tests:latest
 Versions that have been created :
7.3-cli
```


### Known issues
> always add the --replace flag to the build command when you don't have any image locally, otherwise the program will check for an existing image then fail:

```bash
./bin/docker-template build --runtime php --version 7.0.33-fpm  --replace
```
