#!/bin/bash
cd /home/fuzzy/pkg/
gpg --recv-keys 0x1EB2638FF56C0C53
export PATH=$PATH:/usr/bin/core_perl/
sudo -Hu fuzzy aur.sh cower
pacman -U --noconfirm ./cower/cower*.pkg.tar.xz
sudo -Hu fuzzy  aur.sh pacaur
pacman -U --noconfirm ./pacaur/pacaur*.pkg.tar.xz
