FROM php:7.1.0-fpm

LABEL description="This image is used to create continuousphp containers" vendor="continuousphp" version="1.0"

MAINTAINER Pierre Tomasina <pierre.tomasina@continuousphp.com>
MAINTAINER Oswald De Riemaecker <oswald@continuousphp.com>

ENV CONTINUOUSPHP continuousphp
ENV TERM xterm

ENV WHITE "\x1B033[0;02m"
ENV GREEN "\x1B[1;32m"
ENV RED "\x1B[1;31m"
ENV YELLOW "\x1B[1;33m"
ENV BLUE "\x1B[1;34m"
ENV PINK "\x1B[1;35m"
ENV CYAN "\x1B[1;36m"
ENV NORMAL "\x1B[0;39m"

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    ca-certificates \
    rpm \
    zip \
    unzip \
    curl \
    vim \
    git \
    build-essential \
    sudo \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

ADD files/01_nodoc /etc/dpkg/dpkg.cfg.d/

RUN mkdir /var/run/sshd
RUN echo 'root:cphp' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

#
# Setting cphp user
#
RUN groupadd cphp
RUN useradd -m -g cphp -p "$1$hDIpGJlN$OqzLQ9sxi9rBDi4GH7kid1" -s /bin/bash cphp 
ADD files/sudoer_cphp /etc/sudoers.d/cphp
USER cphp
RUN mkdir -p /home/cphp/var
ADD files/scripts/git_ssh.sh /usr/bin/git_ssh.sh
USER root
ADD files/scripts/git-env.sh /etc/profile.d
ADD files/scripts/ssh-agent.sh /etc/profile.d
ADD files/scripts/continuousphp-env.sh /etc/profile.d
USER cphp
ADD files/authorized_keys /home/cphp/.ssh/authorized_keys
USER root
RUN mkdir -p /var/www
RUN ln -s /home/cphp/var/www /var/www/html

#
# Bootstrap CPHP Dependencies
#
COPY files/scripts/bootstrap.sh /tmp/
COPY files/.profile /home/cphp/.profile
RUN /tmp/bootstrap.sh
#
# Installing "n" the nodejs mutli versions support
#
USER cphp
RUN curl -L https://raw.githubusercontent.com/mklement0/n-install/stable/bin/n-install | bash -s -- -y
USER root

#
# Install pip and famous tools coid
#
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install awscli

#
# Installing Azure Cli
#
#RUN source /home/cphp/.bashrc ; npm install azure-cli
RUN su - cphp -c "npm install -g azure-cli"

#
# Install terraform tools
#
RUN cd /usr/local/bin && curl -O https://releases.hashicorp.com/terraform/0.6.16/terraform_0.6.16_linux_amd64.zip ; \
    unzip terraform_0.6.16_linux_amd64.zip \
    && rm -f terraform_0.6.16_linux_amd64.zip

USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/sstephenson/bats.git
WORKDIR bats
RUN ./install.sh /usr/local
WORKDIR /

CMD [ "bats", "test.bats" ]