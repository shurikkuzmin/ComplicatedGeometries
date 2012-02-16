#import numpy
import os
import subprocess
def modify_file(radius_str,wall_gradient_str):
    f=open("binary.pbs","r+")
    f2=open("binary_new.pbs","w")
    for counter,line in enumerate(f):
        if line.find("TOCHANGE")!=-1:
            line=line.replace("TOCHANGE1",radius_str)
            line=line.replace("TOCHANGE2",wall_gradient_str)
        f2.write(line)
            
    f.close()
    f2.close()

def modify_file_wall(radius_str,wall_gradient_str):
    f=open("binary_wall.pbs","r+")
    f2=open("binary_wall_new.pbs","w")
    for counter,line in enumerate(f):
        if line.find("TOCHANGE")!=-1:
            line=line.replace("TOCHANGE1",radius_str)
            line=line.replace("TOCHANGE2",wall_gradient_str)
        f2.write(line)
            
    f.close()
    f2.close()


def run_simulations():
    radii_str=[str(x) for x in range(5,40,5)]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        subprocess.call(['cp','main.out',radius_str+"/"])
        subprocess.call(['cp','main_wall.out',radius_str+"/"])
        subprocess.call(['cp','binary.pbs',radius_str+"/"])
        subprocess.call(['cp','binary_wall.pbs',radius_str+"/"])
        os.chdir(radius_str)
        wall_gradients_str=["Grad"+str(x) for x in range(-45,50,5)]
        wall_gradients=[str(x) for x in range(-45,50,5)]
        
        for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
            subprocess.call(['mkdir','-p',wall_gradient_str])
            subprocess.call(['cp','main.out',wall_gradient_str+"/"])
            subprocess.call(['cp','main_wall.out',wall_gradient_str+"/"])
            subprocess.call(['cp','binary.pbs',wall_gradient_str+"/"])
            subprocess.call(['cp','binary_wall.pbs',wall_gradient_str+"/"])
            os.chdir(wall_gradient_str)
            wall_gradient=0.01*float(wall_gradients[wall_counter])
            modify_file(radius_str,str(wall_gradient))
            modify_file_wall(radius_str,str(wall_gradient))
            #subprocess.call(['qsub','binary_new.pbs'])
            #subprocess.call(['qsub','binary_wall_new.pbs'])
 
            os.chdir("..")
        os.chdir("..")

if __name__=="__main__":
    #modify_file()
    run_simulations()
