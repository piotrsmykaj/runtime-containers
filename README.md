<a href="http://continuous.lu">
  <img src="https://app.continuousphp.com/assets/logos/continuousphp.svg" alt="ContinuousPHP" width="250px" align="right"/>
</a>

<p align="left">
  <a href="https://continuousphp.com/git-hub/continuousphp/runtime-container"><img alt="Build Status" src="https://status.continuousphp.com/git-hub/continuousphp/cli?token=8eb1b41e-343a-41b5-b68f-179fb1ce1ffe&branch=master" /></a>
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
      Docker Template:
        The 

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
	- [] Conditional statement of a runtime variable ( when runtime are build, I want condition the integration of the statement if variable condition are meet, like version of runtime php-7.1)

#### Additional files

When ADD or COPY are used in components, the specified must be stored inside a "files" directory but the written path must
follow the syntax: files/component_name/path_to_files_in_files_directory

## Runtime

### Runtime Configuration

The configuration must have the following functionality:
1. variable version for `FROM` instruction
2. flavours parsing to know witch flavour of components must be included
3. list of components to includes

### Runtime Tests

The tests bats must be build based on each runtime build, use template like this

```
FROM %continuous:runtime-version
USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/bats-core/bats-core /tmp/bats-core \
    && cd /tmp/bats-core \
    && ./install.sh /usr/local
CMD [ "bats", "/test.bats" ]
```

