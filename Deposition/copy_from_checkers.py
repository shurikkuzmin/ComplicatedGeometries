#import numpy
import os
import subprocess

def run_simulations():
    radii_str=["20"]
    forces=[0.000005,0.00001,0.00002]
    forces_str=["5","10","20"]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        os.chdir(radius_str)
        wall_gradients_str=["Grad"+str(x) for x in range(-40,50,20)]
        wall_gradients=[str(x) for x in range(-40,50,20)]
        
        for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
            subprocess.call(['mkdir','-p',wall_gradient_str])
            os.chdir(wall_gradient_str)
            for force_counter,force in enumerate(forces):
                subprocess.call(['mkdir','-p',forces_str[force_counter]])
                os.chdir(forces_str[force_counter])
                for time_counter in range(0,100001,2000):
                    file_name="vtk"+"0"*(7-len(str(time_counter)))+str(time_counter)+".vtk"
                    subprocess.call(["scp","shurik@checkers.westgrid.ca:/home/shurik/Deposition/"+radius_str+"/"+wall_gradient_str+"/"+forces_str[force_counter]+"/"+file_name,"."])
                os.chdir("..")
                #subprocess.call(['qsub','binary_new.pbs'])
 
            os.chdir("..")
        os.chdir("..")

if __name__=="__main__":
    #modify_file()
    run_simulations()
