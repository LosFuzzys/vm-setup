FROM base/archlinux

RUN useradd -m -g users -G wheel fuzzy

RUN sed -e 's/#Color/Color/g' -i /etc/pacman.conf

# install stuff

# force creation of gpg/dirmngr dirs for root
ADD files/mirrorlist /etc/pacman.d/mirrorlist
RUN dirmngr < /dev/null
RUN pacman-key --refresh-keys
RUN pacman -Syu --noconfirm
RUN pacman-db-upgrade
RUN pacman -Scc --noconfirm
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
RUN chmod +x /usr/local/bin/aur.sh

USER fuzzy
RUN mkdir -p /home/fuzzy/pkg/
WORKDIR /home/fuzzy/pkg/
RUN gpg --recv-keys 0x1EB2638FF56C0C53
ENV PATH $PATH:/usr/bin/core_perl/
USER fuzzy
RUN aur.sh cower
USER root
RUN pacman -U --noconfirm ./cower/cower*.pkg.tar.xz
USER fuzzy
RUN aur.sh pacaur
USER root
RUN pacman -U --noconfirm ./pacaur/pacaur*.pkg.tar.xz

USER fuzzy
RUN mkdir -p /home/fuzzy/bin/
RUN mkdir -p /home/fuzzy/src/

WORKDIR /home/fuzzy/

ADD files/pyenv.sh /home/fuzzy/.pyvenv.sh
ENV PATH $PATH:/home/fuzzy/bin/

# clone ctf-tools repo
RUN git clone -b archlinux https://github.com/LosFuzzys/ctf-tools.git
RUN /home/fuzzy/ctf-tools/manage-tools setup
# everyone needs these ;)
RUN /home/fuzzy/ctf-tools/manage-tools -s install radare
RUN /home/fuzzy/ctf-tools/manage-tools -s install binjitsu

# Add some dotfiles
USER fuzzy
ADD files/gdbinit /home/fuzzy/.gdbinit
ADD files/zshrc /home/fuzzy/.zshrc
ADD files/profile /home/fuzzy/.profile
ADD files/tmux.conf /home/fuzzy/.tmux.conf

# Update system again
USER root
ADD files/10-ptrace.conf /etc/sysctl.d/
RUN pacman -Syu --noconfirm
RUN pacman -Scc --noconfirm
# change the shell for primary user
RUN chsh -s /usr/bin/zsh fuzzy

# prepare for launch
USER fuzzy
VOLUME ctf
WORKDIR /ctf
ENTRYPOINT tmux
