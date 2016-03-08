#!/bin/sh
pacman -Sy --needed --noconfirm $@
pacman -Scc --noconfirm
