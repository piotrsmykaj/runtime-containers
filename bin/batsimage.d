USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/sstephenson/bats.git
WORKDIR bats
RUN ./install.sh /usr/local
WORKDIR /

CMD [ "bats", "test.bats" ]