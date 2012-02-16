import numpy
import os
import subprocess

def copy_files():
    subprocess.call(['scp','binary.cpp','shurik@checkers.westgrid.ca:/home/shurik/ComplicatedBunch/'])
    subprocess.call(['scp','binary_wall.cpp','shurik@checkers.westgrid.ca:/home/shurik/ComplicatedBunch/'])
    subprocess.call(['scp','govern.py','shurik@checkers.westgrid.ca:/home/shurik/ComplicatedBunch/'])
    subprocess.call(['scp','binary.pbs','shurik@checkers.westgrid.ca:/home/shurik/ComplicatedBunch/'])
    subprocess.call(['scp','binary_wall.pbs','shurik@checkers.westgrid.ca:/home/shurik/ComplicatedBunch/'])

if __name__=="__main__":
    #modify_file()
    #run_simulations()
    #copy_files("42",5,4)
    #copy_files("60",10,5)
    copy_files()
