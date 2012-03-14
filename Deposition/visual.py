import numpy
import pylab
import time
import vtk
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
                  
        fig=pylab.figure(1)
        pylab.imshow(phase)
        #fig.show()
        pylab.savefig(file_name[:-4]+".jpg")
        pylab.close()
        print file_name+" is processed"

def visualize():
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
            wall_gradient=0.01*float(wall_gradients[wall_counter])
            for force_counter,force in enumerate(forces):
                subprocess.call(['mkdir','-p',forces_str[force_counter]])
                os.chdir(forces_str[force_counter])
                print wall_gradient_str+"/"+forces_str[force_counter]
                
                read_vtk()    

                os.chdir("..")
 
            os.chdir("..")
        os.chdir("..")
 

    
if __name__=="__main__":
    visualize()