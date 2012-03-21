import numpy
import os
import subprocess

def copy_files():
    subprocess.call(['scp','binary.cpp','shurik@checkers.westgrid.ca:/home/shurik/ViscosityDeposition/'])
    subprocess.call(['scp','govern.py','shurik@checkers.westgrid.ca:/home/shurik/ViscosityDeposition/'])
    subprocess.call(['scp','binary.pbs','shurik@checkers.westgrid.ca:/home/shurik/ViscosityDeposition/'])
 
if __name__=="__main__":
    copy_files()
