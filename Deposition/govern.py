#import numpy
import os
import subprocess
def modify_file(radius_str,wall_gradient_str,force_str):
    f=open("binary.pbs","r+")
    f2=open("binary_new.pbs","w")
    for counter,line in enumerate(f):
        if line.find("TOCHANGE")!=-1:
            line=line.replace("TOCHANGE1",radius_str)
            line=line.replace("TOCHANGE2",wall_gradient_str)
            line=line.replace("TOCHANGE3",force_str)
        f2.write(line)
            
    f.close()
    f2.close()


def run_simulations():
    radii_str=["20"]
    forces=[0.000005,0.00001,0.00002]
    forces_str=["5","10","20"]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        subprocess.call(['cp','main.out',radius_str+"/"])
        subprocess.call(['cp','binary.pbs',radius_str+"/"])
        os.chdir(radius_str)
        wall_gradients_str=["Grad"+str(x) for x in range(-40,50,20)]
        wall_gradients=[str(x) for x in range(-40,50,20)]
        
        for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
            subprocess.call(['mkdir','-p',wall_gradient_str])
            subprocess.call(['cp','main.out',wall_gradient_str+"/"])
            subprocess.call(['cp','binary.pbs',wall_gradient_str+"/"])
            os.chdir(wall_gradient_str)
            wall_gradient=0.01*float(wall_gradients[wall_counter])
            for force_counter,force in enumerate(forces):
                subprocess.call(['mkdir','-p',forces_str[force_counter]])
                subprocess.call(['cp','main.out',forces_str[force_counter]+"/"])
                subprocess.call(['cp','binary.pbs',forces_str[force_counter]+"/"])
                os.chdir(forces_str[force_counter])
                modify_file(radius_str,str(wall_gradient),str(force))
                os.chdir("..")
                #subprocess.call(['qsub','binary_new.pbs'])
 
            os.chdir("..")
        os.chdir("..")

if __name__=="__main__":
    #modify_file()
    run_simulations()
