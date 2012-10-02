import vtk
import numpy
import pylab
from operator import itemgetter
import math
from scipy.optimize import fsolve

def read_file_wall(file_name):

    gridreader = vtk.vtkStructuredGridReader() 
    gridreader.SetFileName(file_name)
    gridreader.Update()
    
    grid  = gridreader.GetOutput()
    data  = grid.GetPointData()
    points= grid.GetPoints()
    dims  = grid.GetDimensions()
    print dims    
    
    phase_orig=data.GetArray("phase")
    
    #vz=numpy.zeros([dims[1],dims[2]])
    #vy=numpy.zeros([dims[1],dims[2]])
    #vx=numpy.zeros([dims[1],dims[2]])
    phase=numpy.zeros([dims[0],dims[1]])
    
    #print vz.shape
    #print vy.shape

    for coorx in range(0,dims[0]):
        for coory in range(0,dims[1]):
            counter=coory*dims[0]+coorx
            phase[coorx,coory]=phase_orig.GetTuple1(counter)
    print phase
    pylab.figure()
    pylab.imshow(phase)
    pylab.figure()
    cont=pylab.contour(phase,levels=[0.0,1.4])

    path0=cont.collections[0].get_paths()[0]
    path1=cont.collections[1].get_paths()[0]
    coor_drop=path0.vertices
    coor_wall=path1.vertices    
    pylab.figure()    
    pylab.plot(coor_drop[:,0],coor_drop[:,1],"+")
    pylab.plot(coor_wall[:,0],coor_wall[:,1],"o")
    center=phase[:,dims[1]/2]
    min_coor_wall=min(numpy.where(center>1.2)[0])
    max_coor_wall=max(numpy.where(center>1.2)[0])
    
    pylab.figure()
    coor_one_droplet=numpy.where(coor_drop[:,1]>max_coor_wall)
    print coor_drop[coor_one_droplet,0].ravel()
    coorx=coor_drop[coor_one_droplet,0].ravel()
    coory=coor_drop[coor_one_droplet,1].ravel()
    coor=zip(coorx,coory)
    coor=numpy.array(sorted(coor, key=itemgetter(0)))
    pylab.plot(coor[:,0],coor[:,1],"o")    
    window=5    
    vecx=coor[window,0]-coor[0,0]
    vecy=coor[window,1]-coor[0,1]

    return 180.0/math.pi*math.atan2(vecy,vecx)

def read_file_wall_clean(file_name):

    gridreader = vtk.vtkStructuredGridReader() 
    gridreader.SetFileName(file_name)
    gridreader.Update()
    
    grid  = gridreader.GetOutput()
    data  = grid.GetPointData()
    points= grid.GetPoints()
    dims  = grid.GetDimensions()
    
    phase_orig=data.GetArray("phase")
    
    phase=numpy.zeros([dims[1],dims[0]])

    for coorx in range(0,dims[0]):
        for coory in range(0,dims[1]):
            counter=coory*dims[0]+coorx
            phase[coory,coorx]=phase_orig.GetTuple1(counter)
    pylab.figure(99)    
    cont=pylab.contour(phase,levels=[0.0,1.4])
    
    path0=cont.collections[0].get_paths()[0]
    path1=cont.collections[1].get_paths()[0]
    coor_drop=path0.vertices
    coor_wall=path1.vertices
    #pylab.figure()
    #pylab.plot(coor_drop[:,0],coor_drop[:,1])
    center=phase[:,dims[0]/2]
    #pylab.figure()
    #pylab.plot(center)
    min_coor_wall=min(numpy.where(center>1.2)[0])
    max_coor_wall=max(numpy.where(center>1.2)[0])
    
    threshold=1.0
    coor_one_droplet=numpy.where(coor_drop[:,0]>max_coor_wall+threshold)
    coory=coor_drop[coor_one_droplet,0].ravel()
    coorx=coor_drop[coor_one_droplet,1].ravel()
    #pylab.figure()
    #pylab.plot(coorx,coory)
    coor=numpy.array(zip(coorx,coory))
    #coor=numpy.array(sorted(coor, key=itemgetter(0)))
    #coor=numpy.fliplr(coor)
    #pylab.figure()
    #pylab.plot(coor[:,0],coor[:,1])
    print coor[0,0],coor[0,1]
    window=5    
    vecx=coor[window,0]-coor[0,0]
    vecy=coor[window,1]-coor[0,1]

    return 180.0/math.pi*math.atan2(vecy,vecx)

def f(x,wall_gradient):
    alpha=math.acos(math.sin(x)*math.sin(x))
    return math.sqrt(2.0)*numpy.sign(0.5*math.pi-x)*math.sqrt(math.cos(alpha/3.0)*(1.0-math.cos(alpha/3.0)))+wall_gradient


def wall_analysis():
    angles=[]
    gradients=numpy.arange(-45,45,5)
    
    for gradient in gradients:
        file_name="20/Grad"+str(gradient)+"/vtk_wall0020000.vtk"
        angles.append(read_file_wall_clean(file_name))
    #print angles
    grads=numpy.arange(-0.45,0.46,0.01)
    theor=[]    
    for counter,grad in enumerate(grads):
        theor.append(180.0/math.pi*fsolve(f,math.pi/120*counter,args=(grad)))   
    pylab.figure(1)    
    pylab.plot(0.01*gradients,angles)    
    pylab.plot(grads,theor,"+")
    pylab.ylim(ymin=0.0,ymax=180.0)
    pylab.savefig("main_curve.eps",format="EPS",dpi=300.0)
    pylab.figure(99)
    pylab.savefig("different_boxes.eps",format="EPS",dpi=300.0)

    
def read_file_circle(file_name):
    radius=50    

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
            phase[coory,coorx]=phase_orig.GetTuple1(counter)
    print phase
    #pylab.figure()
    #pylab.imshow(phase)
    pylab.figure()
    cont=pylab.contour(phase,levels=[0.0,1.4])

    path0=cont.collections[0].get_paths()[0]
    path1=cont.collections[1].get_paths()[0]
    coor_drop=path0.vertices
    coor_wall=path1.vertices    
    pylab.figure()    
    pylab.plot(coor_drop[:,0],coor_drop[:,1],"+")
    #pylab.figure()    
    #pylab.plot(coor_wall[:,0],coor_wall[:,1],"o")
    newx=[]
    newy=[]
    centerx=(dims[0]-1)/2
    centery=(dims[1]-1)/2
    for counter in range(0,len(coor_drop[:,0])):
        if ((coor_drop[counter,0]-centerx)**2+(coor_drop[counter,1]-centery)**2)>radius*radius+1:
            newx.append(coor_drop[counter,0])
            newy.append(coor_drop[counter,1])
    
    
    #We need to shift array to find the beginning of the curve
    counter=0
    dist=0.0    
    while dist<10:
        dist=(newx[counter+1]-newx[counter])**2+(newy[counter+1]-newy[counter])**2
        counter=counter+1
    newx=numpy.roll(newx,-counter)
    newy=numpy.roll(newy,-counter)
    print counter
    
    #calculate vector
    shift=3
    angles=[]
    vecx=newx[shift]-newx[0]
    vecy=newy[shift]-newy[0]
    pylab.arrow(newx[0],newy[0],-0.3*(newy[0]-centery),0.3*(newx[0]-centerx),linewidth=3)
    
    #calculate dot product to the tangential
    dot_product=-vecx*(newy[0]-centery)+vecy*(newx[0]-centerx)
    cos_angle=dot_product/(radius*numpy.sqrt(vecx*vecx+vecy*vecy))
    angles.append(180.0/math.pi*math.acos(cos_angle))
    
    counter=2
    while (counter<len(newx)-1):
        if (newx[counter+1]-newx[counter])**2+(newy[counter+1]-newy[counter])**2<10:
            counter=counter+1
            continue
        else:
            counter=counter+1
            print "Found new ",newx[counter],newy[counter]
            vecx=newx[counter+shift]-newx[counter]
            vecy=newy[counter+shift]-newy[counter]
            #calculate dot product to the tangential
            print "tangential=",-(newy[counter]-centery),(newx[counter]-centerx)
            pylab.arrow(newx[counter],newy[counter],-0.3*(newy[counter]-centery),0.3*(newx[counter]-centerx),\
                         shape='right',linewidth=3)
            
            dot_product=-vecx*(newy[counter]-centery)+vecy*(newx[counter]-centerx)
            cos_angle=dot_product/(radius*numpy.sqrt(vecx*vecx+vecy*vecy))
            angles.append(180.0/math.pi*math.acos(cos_angle))
            counter=counter+1
            continue
    print angles
            
          
    #center=phase[:,dims[1]/2]
    #min_coor_wall=min(numpy.where(center>1.2)[0])
    #max_coor_wall=max(numpy.where(center>1.2)[0])
    
    #pylab.figure()
    #coor_one_droplet=numpy.where(coor_drop[:,1]>max_coor_wall)
    #print coor_drop[coor_one_droplet,0].ravel()
    #coorx=coor_drop[coor_one_droplet,0].ravel()
    #coory=coor_drop[coor_one_droplet,1].ravel()
    #coor=zip(coorx,coory)
    #coor=numpy.array(sorted(coor, key=itemgetter(0)))
    #pylab.plot(coor[:,0],coor[:,1],"o")    
    #window=5    
    #vecx=coor[window,0]-coor[0,0]
    #vecy=coor[window,1]-coor[0,1]

    #return 180.0/math.pi*math.atan2(vecy,vecx)

gl_counter=0

def read_file_circle_clean(file_name):
    radius=50
    global gl_counter
    gl_counter=gl_counter+1
    styles=["k+","ko","ks","kv","k^","kd","kD","kh"]    

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
            phase[coory,coorx]=phase_orig.GetTuple1(counter)
    print phase

    pylab.figure(99)
    cont=pylab.contour(phase,levels=[0.0,1.4])

    path0=cont.collections[0].get_paths()[0]
    path1=cont.collections[1].get_paths()[0]
    coor_drop=path0.vertices
    coor_wall=path1.vertices    
    newx=[]
    newy=[]

    centerx=(dims[0]-1)/2
    centery=(dims[1]-1)/2
    for counter in range(0,len(coor_drop[:,0])):
        if ((coor_drop[counter,0]-centerx)**2+(coor_drop[counter,1]-centery)**2)>radius*radius+1:
            newx.append(coor_drop[counter,0])
            newy.append(coor_drop[counter,1])
    
    #We need to shift array to find the beginning of the curve
    counter=0
    dist=0.0    
    while dist<10:
        dist=(newx[counter+1]-newx[counter])**2+(newy[counter+1]-newy[counter])**2
        counter=counter+1
    newx=numpy.roll(newx,-counter)
    newy=numpy.roll(newy,-counter)
    print counter
    
    pylab.figure(100)
    dist=0.0
    while dist<10:
        dist=(newx[counter+1]-newx[counter])**2+(newy[counter+1]-newy[counter])**2
        counter=counter+1
    
    pylab.plot(newx[:counter],newy[:counter],"k--",linewidth=3)
    if gl_counter<2:
        pylab.plot(coor_wall[:,0],coor_wall[:,1],"k-",linewidth=3)
    pylab.ylabel(r'''$y$''',fontsize=20)
    pylab.xlabel(r'''$x$''',fontsize=20)
    pylab.ylim((60,240))
    pylab.xlim((60,240))
    pylab.title("Droplet shapes on a curved substrate",fontsize=20)
    pylab.savefig("droplet_shapes_curved_substrates",format="EPS")
    
    pylab.figure(99)
    #calculate vector
    shift=3
    angles=[]
    vecx=newx[shift]-newx[0]
    vecy=newy[shift]-newy[0]
    pylab.arrow(newx[0],newy[0],-0.3*(newy[0]-centery),0.3*(newx[0]-centerx),linewidth=3)
    
    #calculate dot product to the tangential
    dot_product=-vecx*(newy[0]-centery)+vecy*(newx[0]-centerx)
    cos_angle=dot_product/(radius*numpy.sqrt(vecx*vecx+vecy*vecy))
    angles.append(180.0/math.pi*math.acos(cos_angle))
    
    counter=2
    while (counter<len(newx)-1):
        if (newx[counter+1]-newx[counter])**2+(newy[counter+1]-newy[counter])**2<10:
            counter=counter+1
            continue
        else:
            counter=counter+1
            print "Found new ",newx[counter],newy[counter]
            vecx=newx[counter+shift]-newx[counter]
            vecy=newy[counter+shift]-newy[counter]
            #calculate dot product to the tangential
            print "tangential=",-(newy[counter]-centery),(newx[counter]-centerx)
            pylab.arrow(newx[counter],newy[counter],-0.3*(newy[counter]-centery),0.3*(newx[counter]-centerx),\
                         shape='right',linewidth=3)
            
            dot_product=-vecx*(newy[counter]-centery)+vecy*(newx[counter]-centerx)
            cos_angle=dot_product/(radius*numpy.sqrt(vecx*vecx+vecy*vecy))
            angles.append(180.0/math.pi*math.acos(cos_angle))
            counter=counter+1
            continue
    return angles

def circle_analysis():
    angles=[]
    gradients=numpy.arange(-40,41,10)
    
    for gradient in gradients:
        file_name="20/Grad"+str(gradient)+"/vtk0020000.vtk"
        angles.append(read_file_circle_clean(file_name))
    #print angles
    grads=numpy.arange(-0.45,0.46,0.01)
    theor=[]    
    for counter,grad in enumerate(grads):
        theor.append(180.0/math.pi*fsolve(f,math.pi/120*counter,args=(grad)))   
    pylab.figure(1)    
    angles=numpy.array(angles)    
    #pylab.plot(0.01*gradients,angles[:,0],"k+")
    #pylab.plot(0.01*gradients,angles[:,1],"ko")
    gradients=0.01*gradients
    pylab.plot(gradients,angles[:,2],"ko",markersize=8)
    theor=numpy.array(theor)
    good_ind=numpy.where(numpy.logical_and(theor>5,theor<170))
    theor=theor[good_ind]
    grads=grads[good_ind]
    pylab.plot(grads,theor,"k-",linewidth=3)
    numpy.savetxt("theoretical.dat",zip(grads.tolist(),theor.tolist()))
    numpy.savetxt("circle.dat",zip(gradients.tolist(),angles[:,2].tolist()))
  
    pylab.ylim(ymin=0.0,ymax=180.0)
    pylab.savefig("main_curve_circle.eps",format="EPS",dpi=300.0)
    pylab.legend(["Analytical","Simulations"])
    pylab.figure(99)
    pylab.savefig("different_boxes_circle.eps",format="EPS",dpi=300.0)

def circle_figures():
    anals=numpy.loadtxt("theoretical.dat")
    sims=numpy.loadtxt("circle.dat")
    pylab.plot(anals[:,0],anals[:,1],"k-",linewidth=3)
    pylab.plot(sims[:,0],sims[:,1],"ko",markersize=8)
    pylab.legend(["Analytical","Simulations"])
    pylab.ylim(ymin=0.0,ymax=180.0)
    pylab.xlabel(r'''$\partial_{\perp}\phi$''',fontsize=20)
    pylab.ylabel(r'''$\theta_{w}$''',fontsize=20)
    pylab.savefig("main_curve_circle.eps",format="EPS",dpi=300.0)
    pylab.title("Contact angle",fontsize=30)
    
if __name__=="__main__":
    #file_name="vtk_wall0010000.vtk"    
    #read_file_wall(file_name)
    #wall_analysis()

    file_name="20/Grad-35/vtk0020000.vtk"
    #read_file_circle(file_name)
    circle_analysis()
    #circle_figures()
    pylab.show()