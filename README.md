# Introduction
This repository is for the scientists and researchers who want to run the offline RRTMG code to do some calculation, such as the CFRAM analysis (e.g., Dynamical greenhouse-plus feedback and polar warming amplification. Part II: Meridional and vertical asymmetries of the global warming by Lu and Cai (2007)). The repository includes the modified RRTMG files written in Fortran, and the python function to run the offline RRTMG code. 

# Getting started
You need to be able to run the CESM model, or another GCM which used RRTMG radiation scheme. You also need the climlab (https://github.com/climlab/climlab). 

# Codes
Radiation.F90, radsw.F90, radlw.F90 are the modified RRTMG codes I write to output the necessary inputs to the offline RRTMG, including the specific humidity, ozone, cloud, etc. Offline_RRTMG.ipynb includes all the functions you need to do the offline calculation. The example code is given by offline7.py. The calculation may take some time, be patient. 

# Author
Li Zhuo
