#!/usr/bin/env zsh

# Ask for the administrator password upfront
sudo -v

# Keep-alive: update existing `sudo` time stamp until `.macos` has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

# basic necessities
sudo port -N install zsh \
    +mp_completion \
    curl \
    curl-ca-bundle \
    coreutils \
    cmake \
    git \
    git-lfs \
    gnupg2 \
    gnuplot \
    gnutls \
    git \
    curl \
    wget \
    bash-completion  \
        zsh-completions

# for code compilation
sudo port -N install gcc9 \
    cctools

# some programming languages
sudo port -N install go
sudo port -N install perl5
sudo port -N install qt5

# additional stuff
sudo port -N install vtk
sudo port -N install tcl
sudo port -N install tk

# python
sudo port -N install python27 \
    py27-virtualenv \
    py27-virtualenvwrapper \
    py27-pip \
    python2_select
sudo port -N install python37 \
    py37-virtualenv \
    py37-virtualenvwrapper \
    py37-pip \
    python3_select
sudo port -N install py37-pygments \
    py37-tox \
    py37-wheel \
    py37-setuptools \
    py37-click \
    py37-flake8 \
    py37-virtualenvwrapper
sudo port -N install pip_select

# setting defaults
sudo port select --set python python37
sudo port select --set python3 python37
sudo port select --set python2 python27
sudo port select --set virtualenv virtualenv37
sudo port select --set pip pip37
sudo port select --set pip3 pip37
sudo port select --set pip2 pip37
sudo port select --set pycodestyle pycodestyle-py37
sudo port select --set flake8 flake8-37
sudo port select --set pyflakes py37-pyflakes
sudo port select --set pygments py37-pygments
sudo port select --set sphinx py37-sphinx
sudo port select --set tox tox37
