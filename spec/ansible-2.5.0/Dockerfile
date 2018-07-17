FROM centos:7

MAINTAINER Juan Manuel Parrilla <jparrill@redhat.com>

RUN dnf clean all && \
    dnf install -y epel-release && \
    dnf install -y PyYAML python-jinja2 python-httplib2 python-keyczar python-paramiko python-setuptools git python-pip sshpass && \
    dnf install -y gcc libffi-devel python-devel openssl-devel && \
    dnf clean all

RUN mkdir /etc/ansible/ && \
    echo -e '[local]\nlocalhost' > /etc/ansible/hosts

RUN pip install "ansible-lint" "testinfra" "shade" "etcd" "molecule" "ansible==2.5.0" --no-cache-dir