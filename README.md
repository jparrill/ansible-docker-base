Ansible-Docker-Base
===================
[![](https://images.microbadger.com/badges/license/padajuan/ansible-docker-base.svg)](http://microbadger.com/images/padajuan/ansible-docker-base)
[![](https://images.microbadger.com/badges/image/padajuan/ansible-docker-base.svg)](http://microbadger.com/images/padajuan/ansible-docker-base)

Docker containers for different Ansible versions.

The image purpose is related to make different tests with different versions of Ansible and verify backward compatibility

[Dockerhub](https://hub.docker.com/r/padajuan/ansible-docker-base/)

Also there is official images of it, just check the [URLs](https://hub.docker.com/search/?q=ansible&page=1&isAutomated=0&isOfficial=0&pullCount=1&starCount=0)

## Features added
Installed new packages with pip to allow testing on destination nodes.
- ansible-lint
- testinfra (to use ansible as a backend)
- python-shade modules to manage openstack

## Why not different Virtual Envs?
If your base release are Ansible 2.0 you cannot install a 1.9 version of Ansible because it Dependency libraries

Hope this be useful for you.

Enjoy!.

## Update

Spec files revamped, now the __builder.py__ script based will get all ansible versions from pip and create the Dockerfiles in the proper folder waiting for a DockerHub build.

Hope this help
