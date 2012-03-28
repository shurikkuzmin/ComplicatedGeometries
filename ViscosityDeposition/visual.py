import numpy
import pylab
import time
#import vtk
import subprocess
import os

def read_vtk():
    for counter in range(0,100000,2000):
        file_name="vtk00"+"0"*(5-len(str(counter)))+str(counter)+".vtk"
       
        gridreader = vtk.vtkStructuredGridReader() 
        gridreader.SetFileName(file_name)
        gridreader.Update()

        grid  = gridreader.GetOutput()
        data  = grid.GetPointData()
        points= grid.GetPoints()
        dims  = grid.GetDimensions()
        print dims    

        phase_orig=data.GetArray("phase")
        phase=numpy.zeros([dims[0],dims[1]])

        for coorx in range(0,dims[0]):
            for coory in range(0,dims[1]):
                 counter=coory*dims[0]+coorx
                 phase[coorx,coory]=phase_orig.GetTuple1(counter)

        phase=phase.transpose()
                  
        fig=pylab.figure(1)
        pylab.imshow(phase)
        #fig.show()
        pylab.savefig(file_name[:-4]+".jpg")
        pylab.close()
        print file_name+" is processed"

def visualize():
    radii_str=["20"]
    forces=[0.000001,0.000002,0.000003,0.000004,0.000005]
    forces_str=["1","2","3","4","5"]
    viscosity_ratios=[5,10,15,20]
    wall_gradients_str=["Grad"+str(x) for x in range(-40,50,10)]
    wall_gradients=[str(x) for x in range(-40,50,10)]

    for radius_str in radii_str:
        subprocess.call(['mkdir','-p',radius_str])
        os.chdir(radius_str)
        
        for viscosity_ratio in viscosity_ratios:
            subprocess.call(['mkdir','-p',str(viscosity_ratio)])
            os.chdir(str(viscosity_ratio))
    
    
            for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
                subprocess.call(['mkdir','-p',wall_gradient_str])
                os.chdir(wall_gradient_str)
                wall_gradient=0.01*float(wall_gradients[wall_counter])
                for force_counter,force in enumerate(forces):
                    subprocess.call(['mkdir','-p',forces_str[force_counter]])
                    os.chdir(forces_str[force_counter])
                    print "Visc"+str(viscosity_ratio)+"/"+wall_gradient_str+"/"+forces_str[force_counter]
                    read_vtk()
                    movie_file="movie_viscratio"+str(viscosity_ratio)+"_"+wall_gradient_str+"-"+forces_str[force_counter]+".avi"
                    subprocess.call(['mencoder','mf://*.jpg','-ovc','lavc','-mf','fps=5','-o',movie_file])    

                    os.chdir("..")

                os.chdir("..")
            os.chdir("..")
        os.chdir("..")

def visualize_particular_simulation(file_dir):
    os.chdir(file_dir)
    read_vtk()
    
def copy_from_computer(file_visc_dir):
    radii_str=["20"]
    forces=[0.000001,0.000002,0.000003,0.000004,0.000005]
    forces_str=["1","2","3","4","5"]
    viscosity_ratios=[5,10,15,20]
    wall_gradients_str=["Grad"+str(x) for x in range(-40,50,10)]
    wall_gradients=[str(x) for x in range(-40,50,10)]

    for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
        for force_counter,force in enumerate(forces):
            subprocess.call(['scp','shurik@129.128.34.145:/home/shurik/Documents/Projects/ComplicatedGeometries/FilesViscosity/20/'\
            +file_visc_dir+"/"+wall_gradient_str+"/"+forces_str[force_counter]+"/*.avi",'.'])
                    
if __name__=="__main__":
    #file_dir="20/10/Grad-10/5"
    #visualize_particular_simulation(file_dir)   
    #visualize()
    copy_from_computer("10")
    