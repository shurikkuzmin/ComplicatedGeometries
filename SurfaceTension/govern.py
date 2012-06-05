#import numpy
import os
import subprocess
def modify_file(radius_str,wall_gradient_str,force_str,viscosity_ratio_str,surface_ratio_str):
    f=open("binary.pbs","r+")
    f2=open("binary_new.pbs","w")
    for counter,line in enumerate(f):
        if line.find("TOCHANGE")!=-1:
            line=line.replace("TOCHANGE1",radius_str)
            line=line.replace("TOCHANGE2",wall_gradient_str)
            line=line.replace("TOCHANGE3",force_str)
            line=line.replace("TOCHANGE4",viscosity_ratio_str)
            line=line.replace("TOCHANGE5",surface_ratio_str)
        f2.write(line)
            
    f.close()
    f2.close()


def run_simulations():
    radii_str=["10","20","30","40","50"]
    forces=[0.000001,0.000005]
    forces_str=["1","5"]
    viscosity_ratios=[1]
    wall_gradients_str=["Grad"+str(x) for x in range(-20,-19)]
    wall_gradients=[str(x) for x in range(-20,19)]
    surface_ratios_str=["Ratio"+str(0.1*x)[:1]+str(0.1*x)[2:3] for x in range(1,20,3)]
    surface_ratios=[str(0.1*x) for x in range(1,20,3)]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        subprocess.call(['cp','main.out',radius_str+"/"])
        subprocess.call(['cp','binary.pbs',radius_str+"/"])
        os.chdir(radius_str)
        
        for viscosity_ratio in viscosity_ratios:
            subprocess.call(['mkdir','-p',str(viscosity_ratio)])
            subprocess.call(['cp','main.out',str(viscosity_ratio)+"/"])
            subprocess.call(['cp','binary.pbs',str(viscosity_ratio)+"/"])
            os.chdir(str(viscosity_ratio))
        
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
                    for surface_counter,surface_ratio_str in enumerate(surface_ratios_str):
                        subprocess.call(['mkdir','-p',surface_ratio_str])
                        subprocess.call(['cp','main.out',surface_ratio_str+'/'])
                        subprocess.call(['cp','binary.pbs',surface_ratio_str+'/'])
                        os.chdir(surface_ratio_str)
                        modify_file(radius_str,str(wall_gradient),str(force),str(viscosity_ratio),surface_ratios[surface_counter])
                        #subprocess.call(['qsub','binary_new.pbs'])
                        os.chdir("..")
                  
                    os.chdir("..")
 
                os.chdir("..")
            os.chdir("..")
        os.chdir("..")
        


if __name__=="__main__":
    #modify_file()
    run_simulations()
