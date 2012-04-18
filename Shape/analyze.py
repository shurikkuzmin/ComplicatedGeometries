import numpy
import pylab
import vtk
from scipy import interpolate
def read_vtk(file_name):
    #constants of binary liquid model
    aconst=0.04
    kconst=0.04
    
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
    
    pylab.figure()
    pylab.imshow(velx)
    pylab.contour(droplet,levels=[0.0])
    pylab.figure()
    pylab.imshow(vely)
    pylab.contour(droplet,levels=[0.0])
    pylab.figure()
    pylab.title("Droplet shape")
    cont=pylab.contour(droplet,levels=[0.0])
    
    path0=cont.collections[0].get_paths()[0]
    coor_drop=path0.vertices
    #get the largest coordinate and start counting from it
    velx_circle=[]
    ind=-0
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
    pylab.figure()
    pylab.plot(velx_circle)
    
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
    pylab.figure()
    pylab.imshow(bulk_pressure)
    pylab.colorbar()
    #pressure difference - if bubble is nice
    pressure_difference_nice=numpy.mean(bulk_pressure[ydroplet-2:ydroplet+2,xdroplet-2:xdroplet+2])\
                       -numpy.mean(bulk_pressure[98:102,0:5])
    #pressure difference -if bubble is not nice
    pressure_difference_bad=bulk_pressure[ydroplet,int(ind_value+ind_value_other)/2]\
            -numpy.mean(bulk_pressure[98:102,0:5])
    print "Pressure difference nice=",pressure_difference_nice
    print "Pressure difference bad=",pressure_difference_bad
    print "Index=",int(ind+ind_other)/2
    
    #calculate pressure difference averaged
    #take the averaged droplet coordinate
    
        
#    print coor_drop[:,0]
#    print coor_drop[:,1]
#    tck = interpolate.bisplrep(x,y,velx)
#    values = interpolate.bisplev(coor_drop[:,0],coor_drop[:,1],tck)
#    print values
    #print znew  
    #pylab.plot(coor_drop[:,0],coor_drop[:,1],"+")
    #pylab.plot(coor_wall[:,0],coor_wall[:,1],"o")
    #center=phase[:,dims[1]/2]
    #min_coor_wall=min(numpy.where(center>1.2)[0])
    #max_coor_wall=max(numpy.where(center>1.2)[0])

   # pylab.figure()
   # coor_one_droplet=numpy.where(coor_drop[:,1]>max_coor_wall)
   # print coor_drop[coor_one_droplet,0].ravel()
   # coorx=coor_drop[coor_one_droplet,0].ravel()
   # coory=coor_drop[coor_one_droplet,1].ravel()
   # coor=zip(coorx,coory)
   # coor=numpy.array(sorted(coor, key=itemgetter(0)))
   # pylab.plot(coor[:,0],coor[:,1],"o")    
   # window=5    
   # vecx=coor[window,0]-coor[0,0]
   # vecy=coor[window,1]-coor[0,1]
   # 
   # return 180.0/math.pi*math.atan2(vecy,vecx)
                  
#        print "Done with vtk processing"
#        fig=pylab.figure(1)
#        pylab.imshow(phase)
#        #fig.show()
#        pylab.savefig(file_name[:-4]+".jpg")
#        pylab.close()
#        print file_name+" is processed"

if __name__=="__main__":
    file_name="vtk0019000.vtk"
    read_vtk(file_name)
    pylab.show()

