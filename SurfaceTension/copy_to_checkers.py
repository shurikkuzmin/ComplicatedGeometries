import numpy
import os
import subprocess

def copy_files():
    subprocess.call(['scp','binary.cpp','shurik@checkers.westgrid.ca:/home/shurik/SurfaceTension/'])
    subprocess.call(['scp','govern.py','shurik@checkers.westgrid.ca:/home/shurik/SurfaceTension/'])
    subprocess.call(['scp','binary.pbs','shurik@checkers.westgrid.ca:/home/shurik/SurfaceTension/'])
 
if __name__=="__main__":
    copy_files()
