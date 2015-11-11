FROM base/archlinux

RUN useradd -m -g users -G wheel fuzzy

RUN sed -e 's/#Color/Color/g' -i /etc/pacman.conf

# install stuff

RUN pacman-key --refresh-keys
RUN pacman -Syu --noconfirm; pacman-db-upgrade; pacman -Scc --noconfirm
RUN pacman -Syy
ADD pacinstall.sh /usr/local/bin/
# a useful shell
RUN pacinstall.sh sudo zsh grml-zsh-config zsh-syntax-highlighting
# for pacaur
RUN pacinstall.sh expac yajl perl
# native development
RUN pacinstall.sh make clang clang-analyzer clang-tools-extra gcc \
cmake git subversion mercurial gdb lldb patch
# useful tools
RUN pacinstall.sh sqlite3 openssh wget curl rsync nmap tcpdump
# python stuff
RUN pacinstall.sh python python-pip python2 python2-pip python-requests \
python-virtualenv python2-virtualenv python-virtualenvwrapper \
python2-requests python-requests \
ipython ipython2 bpython bpython2 \
libffi python2-cffi
# install node.js
RUN pacinstall.sh nodejs npm
# and a tool for doing mitm
RUN pacinstall.sh mitmproxy
# sagemath for solving crypto tasks might be useful
RUN pacinstall.sh mesa-libgl sagemath

ADD wheel /etc/sudoers.d/

# install pacaur, so that we can fetch AUR packages

#RUN wget -O /usr/local/bin/aur.sh http://aur.sh/ && chmod +x /usr/local/bin/aur.sh
ADD aur.sh /usr/local/bin/aur.sh

USER fuzzy
RUN mkdir -p /home/fuzzy/pkg/
WORKDIR /home/fuzzy/pkg/
RUN gpg --recv-keys 0x1EB2638FF56C0C53
CMD ["env", "PATH=$PATH:/usr/bin/core_perl/", "aur.sh", "cower", "pacaur"]
#RUN aur.sh pacaur cower
USER root
cmd ["pacman", "-U", "--noconfirm", "pacaur*", "cower*"]


USER fuzzy

WORKDIR /home/fuzzy
RUN git clone https://github.com/f0rki/dotvim .vim
WORKDIR /home/fuzzy/.vim
RUN ./clonevundle.sh
CMD ["printf" "\':q!\n:q!\n\'", "|", "vim", "-c", "\'PluginInstall\'"]

RUN mkdir -p /home/fuzzy/bin/
RUN mkdir -p /home/fuzzy/src/

WORKDIR /home/fuzzy/src/

RUN git clone https://github.com/sqlmapproject/sqlmap.git
RUN git clone https://github.com/longld/peda.git
RUN git clone https://github.com/mwielgoszewski/python-paddingoracle.git

RUN git clone https://github.com/radare/radare2
WORKDIR /home/fuzzy/src/radare2
RUN env USE_R2_CAPSTONE=1 sys/user.sh


WORKDIR /home/fuzzy/

USER root
ADD ctf-pip /usr/local/bin/

# we need this for angr build to work
RUN ln -s /usr/lib/libffi-3.2.1/include /usr/include/libffi

USER fuzzy
CMD ["echo", "\"source \$(which virtualenvwrapper.sh)\"", ">>", "/home/fuzzy/.zshrc"]
CMD ["echo", "\"source \$(which virtualenvwrapper.sh)\"", ">>", "/home/fuzzy/.profile"]
CMD ["mkvirtualenv", "-p", "\"$(which python2)\"", "ctf"]
RUN ctf-pip install 'git+https://github.com/Gallopsled/pwntools#egg=pwntools'
RUN ctf-pip install ipython
RUN ctf-pip install hashpumpy
RUN cd ~/src/ && ctf-pip install -e python-paddingoracle
RUN ctf-pip install --upgrade angr


CMD ["echo", "\"source ~/src/peda/peda.py\"", ">>", "~/.gdbinit"]
ADD zshrc /home/fuzzy/.zshrc

USER root
RUN pacman -Scc --noconfirm

USER fuzzy
VOLUME ctf
ENTRYPOINT /usr/bin/zsh
