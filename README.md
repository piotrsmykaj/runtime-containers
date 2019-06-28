# Runtime Container

This repository will define the construction of all the runtime containers for ContinuousPHP CI/CD platform

Architecture:

  1. Components:
      Component are a *Docker template* shared playbook, it can be implemented inside a Runtime platform and have its own test write with `bats`.
      The implementation of the component is made using the docker template script in python.

  2. Runtimes:
      Runtimes represent a platform around the same application goal (Language) like `php`, `javascript`, `ruby`, `python`.

