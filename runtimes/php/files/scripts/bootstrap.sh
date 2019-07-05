#!/bin/bash

export GREEN="\\033[1;32m"
export NORMAL="\\033[0;39m"
export RED="\\033[1;31m"
export PINK="\\033[1;35m"
export BLUE="\\033[1;34m"
export WHITE="\\033[0;02m"
export YELLOW="\\033[1;33m"
export CYAN="\\033[1;36m"

rm /bin/sh && ln -s /bin/bash /bin/sh

bats()
{
echo -e "${CYAN}Installing bats...${NORMAL}"

cd /usr/local/src/
git clone https://github.com/sstephenson/bats.git
cd bats
./install.sh /usr/local
cd ~

which bats || exit 2

echo -e "${CYAN}bats installed !${NORMAL}"
}

profile()
{
cat <<EOF >> $1
	if [ -d "\$HOME/n/bin" ] ; then
		PATH="\$HOME/n/bin:\$PATH"
	fi
EOF
}

bats
profile /home/cphp/.profile
