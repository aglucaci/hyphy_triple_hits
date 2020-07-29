#!/bin/bash
#Last update 05-28-2020

#Download and install HyPhy
git clone https://github.com/veg/hyphy.git hyphy-develop

cd hyphy-develop

cmake ./
make -j MP
#make -j MPI

make install

#Download hyphy standalone analyses
cd ..
git clone https://github.com/veg/hyphy-analyses.git

#End of file




