FROM centos:7

MAINTAINER Juan Manuel Parrilla <jparrill@redhat.com>

RUN yum clean all && \
    yum install -y epel-release && \
    yum install -y PyYAML python-jinja2 python-httplib2 python-keyczar python-paramiko python-setuptools git python-pip sshpass && \
    yum install -y gcc libffi-devel python-devel openssl-devel && \
    yum clean all

RUN mkdir /etc/ansible/ && \
    echo -e '[local]\nlocalhost' > /etc/ansible/hosts

RUN pip install "ansible-lint" "testinfra" "shade" "etcd" "molecule" "ansible==2.2.0" --no-cache-dir