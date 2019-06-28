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
      Runtimes represent a platform around the same application goal (Language) like `php`, `javascript`, `ruby`, `python`.

