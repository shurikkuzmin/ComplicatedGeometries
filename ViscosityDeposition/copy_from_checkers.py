#import numpy
import os
import subprocess

def run_simulations():
    radii_str=["20"]
    forces=[0.000001,0.000002,0.000003,0.000004,0.000005]
    forces_str=["1","2","3","4","5"]
    wall_gradients_str=["Grad"+str(x) for x in range(-40,50,10)]
    wall_gradients=[str(x) for x in range(-40,50,10)]
    viscosity_ratios=[5,10,15,20]
    

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        os.chdir(radius_str)
        for viscosity_ratio in viscosity_ratios:
            subprocess.call(['mkdir','-p',str(viscosity_ratio)])
            os.chdir(str(viscosity_ratio))
        
            for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
                subprocess.call(['mkdir','-p',wall_gradient_str])
                os.chdir(wall_gradient_str)
                for force_counter,force in enumerate(forces):
                    subprocess.call(['mkdir','-p',forces_str[force_counter]])
                    os.chdir(forces_str[force_counter])
                    for time_counter in range(0,100001,2000):
                        file_name="vtk"+"0"*(7-len(str(time_counter)))+str(time_counter)+".vtk"
                        subprocess.call(["scp","shurik@checkers.westgrid.ca:/home/shurik/ViscosityDeposition/"+radius_str+"/"\
                        +str(viscosity_ratio)+"/"+wall_gradient_str+"/"+forces_str[force_counter]+"/"+file_name,"."])
                    os.chdir("..")
                    #subprocess.call(['qsub','binary_new.pbs'])

                os.chdir("..")
            os.chdir("..")
        os.chdir("..")

if __name__=="__main__":
    #modify_file()
    run_simulations()
