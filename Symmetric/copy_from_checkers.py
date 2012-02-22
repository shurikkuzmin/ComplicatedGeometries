#import numpy
import os
import subprocess

def copy_directory(file_name):
    radii_str=[str(file_name)]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        os.chdir(radius_str)
        wall_gradients_str=["Grad"+str(x) for x in range(-45,50,5)]
        wall_gradients=[str(x) for x in range(-45,50,5)]
        
        for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
            subprocess.call(['mkdir','-p',wall_gradient_str])
            os.chdir(wall_gradient_str)
            subprocess.call(['scp','checkers.westgrid.ca:/home/shurik/ComplicatedAnother/'+radius_str\
                             +"/"+wall_gradient_str+"/vtk*0020000.vtk","."])
            os.chdir("..")
        os.chdir("..")

if __name__=="__main__":
    #modify_file()
    copy_directory(20)
