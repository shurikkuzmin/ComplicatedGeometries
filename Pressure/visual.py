import numpy
import matplotlib
matplotlib.use('Agg')
import pylab
import time
import vtk
import subprocess
import os

def read_vtk_one():
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
        print "Done with vtk processing"
        #fig=pylab.figure(1)
        pylab.imshow(phase)
        #fig.show()
        pylab.savefig(file_name[:-4]+".jpg")
        pylab.close()
        print file_name+" is processed"

def visualize():
    radii_str=["10","20","30","40","50"]
    forces=[0.000001] #,0.000003,0.000005]
    forces_str=["1"]#,"3","5"]
    viscosity_ratios=[1]
    wall_gradients_str=["Grad"+str(x) for x in range(-40,50,10)]
    wall_gradients=[str(x) for x in range(-40,50,10)]

    for radius_str in radii_str:
        os.chdir(radius_str)
        
        for viscosity_ratio in viscosity_ratios:
            os.chdir(str(viscosity_ratio))
        
            for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
                os.chdir(wall_gradient_str)
                wall_gradient=0.01*float(wall_gradients[wall_counter])
                for force_counter,force in enumerate(forces):
                    os.chdir(forces_str[force_counter])
                    read_vtk_one()
                    movie_name="movie_"+radius_str+"_"+str(viscosity_ratio)+"_"+wall_gradient_str+"_"+forces_str[force_counter]+".avi"
                    subprocess.call(['mencoder',' mf://*.jpg','-ovc','lavc','-mf','fps=5','-o',movie_name])  
                    os.chdir("..")
          
 
                os.chdir("..")
            os.chdir("..")
            print radius_str,"is done"
        os.chdir("..")
 
def copy_files(force_dir):
    radii_str=["10","20","30","40","50"]
    forces=[0.000001] #,0.000003,0.000005]
    #forces_str=["1"]#,"3","5"]
    viscosity_ratios=[1]
    wall_gradients_str=["Grad"+str(x) for x in range(-40,50,10)]
    wall_gradients=[str(x) for x in range(-40,50,10)]

    for radius_str in radii_str:
        for viscosity_ratio in viscosity_ratios:
            for wall_counter,wall_gradient_str in enumerate(wall_gradients_str):
	        #movie_name="movie_"+radius_str+"_"+str(viscosity_ratio)+"_"+wall_gradient_str+"_"+forces_str[force_counter]+".avi"
	        subprocess.call(['scp','shurik@129.128.34.145:/home/shurik/Documents/Projects/ComplicatedGeometries/Pressure/'+radius_str+'/'+str(viscosity_ratio)+'/'+wall_gradient_str+'/'+force_dir+'/*.avi','.'])  
            print radius_str,"is done"
    
if __name__=="__main__":
    #visualize()
    copy_files("1")
