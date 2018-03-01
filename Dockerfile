FROM centos:7.4.1708
MAINTAINER Olekandr Yarushevskyi

# Python 3.6
RUN yum update -y \
    && yum install -y yum-utils wget \
    && yum -y groupinstall development \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-pip python36u-devel

# Adding sources
ADD ./ /app

WORKDIR /app

# Installing Python third-party libraries
RUN python3.6 -m pip install --upgrade pip \
    && python3.6 -m pip install -r /app/requirements.txt

# Dev tools
RUN python3.6 -m pip install ipython[all] pylint pytest-cov

ENV LC_ALL=en_US.utf8

CMD ["bash"]
