
USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/bats-core/bats-core
WORKDIR bats-core
RUN ./install.sh /usr/local
WORKDIR /

CMD [ "bats", "test.bats" ]
