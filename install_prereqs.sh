#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
  echo "Mac not supported yet, but please add support if possible"

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "Assuming you are running Ubuntu. Now installing via apt-get."
  echo "You will need to enter your password to install things"
  sudo apt-get install scons python-biopython python-matplotlib python-pip \
    python-networkx muscle fasttree clustalw mafft graphviz 

else
  echo "Only OSX and Ubuntu supported at the moment, I'm afraid"
fi

sudo pip install colorbrewer graphviz nestly bioscons

