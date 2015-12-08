#### WARNING: this might be outdated!!!

FROM base/archlinux

CMD ["echo", "Server = http://mirror1.htu.tugraz.at/archlinux/$repo/os/$arch", ">", "/etc/pacman.d/mirrorlist"]

RUN useradd -m -g users -G wheel fuzzy

RUN sed -e 's/#Color/Color/g' -i /etc/pacman.conf

# install stuff

RUN pacman-key --refresh-keys
RUN pacman -Syu --noconfirm; pacman-db-upgrade; pacman -Scc --noconfirm
RUN pacman -Syy
ADD files/pacinstall.sh /usr/local/bin/
# a useful shell
RUN pacinstall.sh sudo zsh grml-zsh-config zsh-syntax-highlighting
# for pacaur
RUN pacinstall.sh expac yajl perl fakeroot base-devel
# native development
RUN pacinstall.sh make clang clang-analyzer clang-tools-extra gcc \
cmake git subversion mercurial gdb lldb valgrind boost boost-libs
# network tools
RUN pacinstall.sh openssh wget curl rsync nmap tcpdump gnu-netcat
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
#RUN pacinstall.sh mesa-libgl sagemath
# some more utility tools
RUN pacinstall.sh tmux vim nano sqlite3

ADD files/wheel /etc/sudoers.d/
RUN chmod 600 /etc/sudoers.d/wheel

# install pacaur, so that we can fetch AUR packages

#RUN wget -O /usr/local/bin/aur.sh http://aur.sh/ && chmod +x /usr/local/bin/aur.sh
ADD files/aur.sh /usr/local/bin/aur.sh
CMD ["chmod", "+x", "/usr/local/bin/aur.sh"]

USER fuzzy
RUN mkdir -p /home/fuzzy/pkg/
WORKDIR /home/fuzzy/pkg/
RUN gpg --recv-keys 0x1EB2638FF56C0C53
CMD ["ls", "-al", "1>&2"]
CMD ["env", "PATH=$PATH:/usr/bin/core_perl/", "aur.sh", "cower", "pacaur"]
CMD ["ls", "-al", "1>&2"]
#RUN aur.sh pacaur cower
USER root
CMD ["pacman", "-U", "--noconfirm", "pacaur*", "cower*"]

USER fuzzy
RUN mkdir -p /home/fuzzy/bin/
RUN mkdir -p /home/fuzzy/src/

WORKDIR /home/fuzzy/src/

# some more tools
RUN git clone https://github.com/sqlmapproject/sqlmap.git
RUN git clone https://github.com/mwielgoszewski/python-paddingoracle.git

RUN git clone https://github.com/radare/radare2
RUN git clone https://github.com/radare/radeco.git
RUN git clone https://github.com/jpenalbae/r2-scripts

# Install radare
WORKDIR /home/fuzzy/src/radare2
CMD ["env", "USE_R2_CAPSTONE=1", "./sys/install.sh"]
# and radeco?
WORKDIR /home/fuzzy/src/radeco
USER root
RUN pacinstall.sh rust cargo
USER fuzzy
#RUN cargo build

# Install peda
RUN git clone https://github.com/longld/peda.git
ADD files/gdb-peda ~/bin/

# Install pwndbg
USER fuzzy
RUN git clone https://github.com/zachriggle/pwndbg.git
ADD files/pwndbg ~/bin/
USER root
RUN pacinstall.sh capstone python2-capstone python3-capstone python2-pycparser

# we need this for angr build to work
USER root
RUN ln -s /usr/lib/libffi-3.2.1/include /usr/include/libffi

USER fuzzy
WORKDIR /home/fuzzy/

ADD files/ctf-pip bin/
ADD files/pyvenv.sh /home/fuzzy/.pyvenv.sh
ENV PATH $PATH:/home/fuzzy/bin/
#CMD ["mkvirtualenv", "-p", "\"$(which python2)\"", "ctf"]
# binjitsu vs. pwntools?
#RUN ctf-pip install 'git+https://github.com/Gallopsled/pwntools#egg=pwntools'
RUN ctf-pip install --upgrade ipython bpython
RUN ctf-pip install --upgrade capstone pycparser
CMD ["ctf-pip", "install", "--upgrade", "\'git+https://github.com/binjitsu/binjitsu.git\'"]
RUN ctf-pip install --upgrade hashpumpy
RUN cd src/ && ctf-pip install -e python-paddingoracle
RUN ctf-pip install --upgrade angr


# install some packages from AUR
#CMD pacaur -Syu --noconfirm metasploit-git

# Add some dotfiles
USER fuzzy
ADD files/gdbinit /home/fuzzy/.gdbinit
ADD files/zshrc /home/fuzzy/.zshrc
ADD files/profile /home/fuzzy/.profile
ADD files/tmux.conf /home/fuzzy/.tmux.conf

WORKDIR /home/fuzzy
RUN git clone https://github.com/f0rki/dotvim ~/.vim
WORKDIR /home/fuzzy/.vim
RUN ./clonevundle.sh
CMD ["printf" "\':q!\n:q!\n\'", "|", "vim", "-c", "\'PluginInstall\'"]
#WORKDIR /home/fuzzy/.vim/bundle/YouCompleteMe
#RUN git submodule update --init --recursive
#RUN python2 install.py --clang-completer --system-boost --system-libclang

# Update system again
USER root
RUN pacman -Syu --noconfirm; pacman -Scc --noconfirm
# change the shell for primary user
RUN chsh -s /usr/bin/zsh fuzzy

# prepare for launch
USER fuzzy
VOLUME ctf
WORKDIR /ctf
ENTRYPOINT tmux
