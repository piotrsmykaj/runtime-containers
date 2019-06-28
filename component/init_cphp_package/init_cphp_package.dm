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
