import numpy
import pylab
import vtk
from scipy import interpolate
def read_vtk(file_name):
    gridreader = vtk.vtkStructuredGridReader() 
    gridreader.SetFileName(file_name)
    gridreader.Update()

    grid  = gridreader.GetOutput()
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
             #density[coorx,coory]=density_orig.GetTuple1(counter)
             velx[coorx,coory]=velocity_orig.GetTuple3(counter)[0]
             vely[coorx,coory]=velocity_orig.GetTuple3(counter)[1]
    phase=phase.transpose()
    #density=density.transpose()
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
    #pylab.figure()  
    x,y=numpy.mgrid[0:dims[1],0:dims[0]]
    print x
    print y
    print velx.shape
#    velx_drop=interp2d(x,y,velx,kind='cubic')
    tck = interpolate.bisplrep(x,y,velx,s=0)
    #znew = interpolate.bisplev(x[:,0],ynew[0,:],tck)
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
    file_name="vtk0018000.vtk"
    read_vtk(file_name)
    pylab.show()

