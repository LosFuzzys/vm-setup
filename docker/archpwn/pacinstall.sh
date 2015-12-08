#!/bin/sh
pacman -Sy --noconfirm $@
pacman -Scc --noconfirm
