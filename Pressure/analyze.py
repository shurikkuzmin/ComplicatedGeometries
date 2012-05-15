import numpy
import pylab
import vtk
from scipy import interpolate
def read_vtk(file_name):
    #constants of binary liquid model
    aconst=0.04
    kconst=0.04
    global call_counter
    #styles=['ks','ks','k+','k+','ko','ko','kv','kv']
    styles=['ks','ko','k+','kD','k*','kH','kv','k^','kh','k-']

    call_counter=call_counter+1
    print call_counter
    
    gridreader = vtk.vtkStructuredGridReader() 
    gridreader.SetFileName(file_name)
    gridreader.SetReadAllScalars(1)
    gridreader.Update()

    grid  = gridreader.GetOutput()
    grid.Update()
    data  = grid.GetPointData()
    points= grid.GetPoints()
    dims  = grid.GetDimensions()
    print dims
    phase_orig=data.GetArray("phase")
    density_orig=data.GetArray("density")
    velocity_orig=data.GetArray("velocity")
    phase=numpy.zeros([dims[0],dims[1]])
    density=numpy.zeros([dims[0],dims[1]])
    velx=numpy.zeros([dims[0],dims[1]])
    vely=numpy.zeros([dims[0],dims[1]])

    for coorx in range(0,dims[0]):
        for coory in range(0,dims[1]):
             counter=coory*dims[0]+coorx
             phase[coorx,coory]=phase_orig.GetTuple1(counter)
             density[coorx,coory]=density_orig.GetTuple1(counter)
             velx[coorx,coory]=velocity_orig.GetTuple3(counter)[0]
             vely[coorx,coory]=velocity_orig.GetTuple3(counter)[1]
    phase=phase.transpose()
    density=density.transpose()
    velx=velx.transpose()
    vely=vely.transpose()
    droplet=numpy.zeros_like(phase)
    positive=numpy.logical_and(phase>=-0.01,phase<1.1)
    droplet[positive]=1
    
    #pylab.figure()
    #pylab.imshow(velx)
    #pylab.contour(droplet,levels=[0.0])
    #pylab.figure()
    #pylab.imshow(vely)
    #pylab.contour(droplet,levels=[0.0])
    pylab.figure(98)
    pylab.title("Droplet shape")
    cont=pylab.contour(droplet,styles[call_counter],levels=[0.0])
    
    pylab.figure(99)
    path0=cont.collections[0].get_paths()[0]
    coor_drop=path0.vertices
    pylab.plot(coor_drop[:,0],coor_drop[:,1],styles[call_counter],markersize=5,markerfacecolor="None")
    #get the largest coordinate and start counting from it
    velx_circle=[]
    ind=0
    ind_value=-100
    ind_other=0
    ind_value_other=1000
    for counter in range(0,len(coor_drop[:,0])):
        if int(coor_drop[counter,1]==dims[1]/2):
            if int(coor_drop[counter,0]>ind_value):
                ind=counter
                ind_value=int(coor_drop[counter,0])
            if int(coor_drop[counter,0]<ind_value_other):
                ind_other=counter
                ind_value_other=int(coor_drop[counter,0])
        velx_circle.append(velx[int(coor_drop[counter,1]),int(coor_drop[counter,0])])
    print "Ind=",ind
    print "Ind_other=",ind_other
    print "Ind value=",ind_value
    print "Ind value ohter=",ind_value_other
    y=coor_drop[:,1]
    x=coor_drop[:,0]
    x=numpy.roll(x,-ind)
    y=numpy.roll(y,-ind)    
    velx_circle=numpy.roll(velx_circle,-ind)
    pylab.figure(100)
    middle_range=128
    velx_range=numpy.arange(0,len(velx_circle))+middle_range-len(velx_circle)/2
    pylab.plot(velx_range,velx_circle,styles[call_counter],markersize=5,markerfacecolor="white")
    pylab.xlim(0,2*middle_range)
    
    bulk_pressure=density/3.0+aconst*(-0.5*phase*phase+3.0/4.0*phase*phase*phase*phase)
    xdom,ydom=numpy.mgrid[0:dims[1],0:dims[0]]
    #clean not involved data for visual representation
    substrate=numpy.where((xdom-dims[1]/2)*(xdom-dims[1]/2)+(ydom-dims[0]/2)*(ydom-dims[0]/2)<31*31)
    bulk_pressure[substrate]=bulk_pressure[1,1]
    bulk_pressure[0,:]=bulk_pressure[1,1]
    bulk_pressure[-1,:]=bulk_pressure[1,1]
    xdroplet=int(numpy.mean(x))
    ydroplet=int(numpy.mean(y))
    print xdroplet
    print ydroplet
    #pylab.figure()
    #pylab.imshow(bulk_pressure)
    #pylab.colorbar()
    #pressure difference - if bubble is nice
    pressure_difference_nice=numpy.mean(bulk_pressure[ydroplet-2:ydroplet+2,xdroplet-2:xdroplet+2])\
                       -numpy.mean(bulk_pressure[98:102,0:5])
    #pressure difference -if bubble is not nice
    pressure_difference_bad=bulk_pressure[ydroplet,int(ind_value+ind_value_other)/2]\
            -numpy.mean(bulk_pressure[98:102,0:5])-(1e-6)*(ind_value+ind_value_other)/2
    print "Pressure difference nice=",pressure_difference_nice
    print "Pressure difference bad=",pressure_difference_bad
    print "Index=",int(ind+ind_other)/2
    return pressure_difference_bad


def compare():
    global call_counter
    call_counter=-1
    file_list=["vtk0035000_R10_Grad-20_F1.vtk","vtk0036000_R10_Grad-20_F1.vtk",
               "vtk0034000_R20_Grad-20_F1.vtk","vtk0035000_R20_Grad-20_F1.vtk",
               "vtk0033000_R30_Grad-20_F1.vtk","vtk0034000_R30_Grad-20_F1.vtk",
               "vtk0033000_R40_Grad-20_F1.vtk","vtk0034000_R40_Grad-20_F1.vtk",
               "vtk0033000_R50_Grad-20_F1.vtk","vtk0032000_R50_Grad-20_F1.vtk"]    		   
    pressures=[]
    for file_name in file_list:
        pressure=read_vtk(file_name)
        pressures.append(pressure)
    pylab.figure(99)
    legs=[x[11:14] for x in file_list]
    pylab.savefig("shape_for_grad-20.eps",format="EPS")
    pylab.legend(legs)
    pylab.figure(100)
    pylab.legend(legs)
    # pylab.savefig("velocities_for_grad0.eps",format="EPS")
    pylab.figure(102)
    print pressures
    pylab.plot([10,10,20,20,30,30,40,40,50,50],pressures,'bs',markersize=8)
    print numpy.mean(pressures)*numpy.arange(1,5)
    pylab.savefig("pressure_for_grad-20.eps",format="EPS")
    pylab.plot([1,2,3,4,5],5*[numpy.mean(pressures)],"r-",linewidth=3)
    pylab.ylim(ymin=0)
    
if __name__=="__main__":
    #file_name="vtk0018000.vtk"
    #read_vtk(file_name)
    compare()
    pylab.show()

