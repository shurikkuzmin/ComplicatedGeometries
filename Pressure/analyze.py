import numpy
import pylab

aconst=0.04
kconst=0.04

def read_vtk(file_name):
    import vtk
    from scipy import interpolate
        
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
    density_one_orig=data.GetArray("density_one_component")
    velocity_orig=data.GetArray("velocity")
    phase=numpy.zeros([dims[0],dims[1]])
    density=numpy.zeros([dims[0],dims[1]])
    density_one=numpy.zeros([dims[0],dims[1]])
    velx=numpy.zeros([dims[0],dims[1]])
    vely=numpy.zeros([dims[0],dims[1]])

    for coorx in range(0,dims[0]):
        for coory in range(0,dims[1]):
             counter=coory*dims[0]+coorx
             phase[coorx,coory]=phase_orig.GetTuple1(counter)
             density[coorx,coory]=density_orig.GetTuple1(counter)
             density_one[coorx,coory]=density_one_orig.GetTuple1(counter)
             velx[coorx,coory]=velocity_orig.GetTuple3(counter)[0]
             vely[coorx,coory]=velocity_orig.GetTuple3(counter)[1]
    phase=phase.transpose()
    density=density.transpose()
    density_one=density_one.transpose()
    velx=velx.transpose()
    vely=vely.transpose()
    
    
    return phase,density,density_one,velx,vely,dims
    
def get_droplet(file_name):

    #constants of binary liquid model
    global call_counter

    call_counter=call_counter+1
    print call_counter

    
    styles=['ks','ko','k+','kD','k*','kH','kv','k^','kh','k-']

    phase,density,density_one,velx,vely,dims=read_vtk(file_name)
    
    droplet=numpy.zeros_like(phase)
    positive=numpy.logical_and(phase>=-0.01,phase<1.1)
    droplet[positive]=1
    
    # First figure is to get coordinates
    pylab.figure(1)
    pylab.title("Droplet shape")
    cont=pylab.contour(droplet,styles[call_counter],levels=[0.0])
    path0=cont.collections[0].get_paths()[0]
    coor_drop=path0.vertices
    #pylab.plot(coor_drop[:,0],coor_drop[:,1],styles[call_counter],markersize=5,markerfacecolor="None")
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
    
    return x,y,density,phase,ind_value,ind_value_other,dims,density_one
    
def get_pressure(file_name):

    x,y,density,phase,ind_value,ind_value_other,dims,density_one=get_droplet(file_name)
     
    # Second figure is to put velocities
    #pylab.figure(2)
    #middle_range=128
    #velx_range=numpy.arange(0,len(velx_circle))+middle_range-len(velx_circle)/2
    #pylab.plot(velx_range,velx_circle,styles[call_counter],markersize=5,markerfacecolor="white")
    #pylab.xlim(0,2*middle_range)
    
    
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
            -1.0/3.0-aconst*0.25
            #-1.0/3.0*density_one[ydroplet,(ind_value+ind_value_other)/2]
            #+1.0/3.0*numpy.mean(density_one[98:102,0:5])\
                    
    print "Pressure difference nice=",pressure_difference_nice
    print "Pressure difference bad=",pressure_difference_bad
    return pressure_difference_bad,density[ydroplet,int(ind_value+ind_value_other)/2],\
           density_one[ydroplet,int(ind_value+ind_value_other)/2],\
           phase[ydroplet,int(ind_value+ind_value_other)/2]

def read_all_pressures(file_name):

    x,y,density,phase,ind_value,ind_value_other,dims=get_droplet(file_name)
    # We calculate pressures here   
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
    pressure_inside_droplet=bulk_pressure[ydroplet,int(ind_value+ind_value_other)/2]
    pressure_outside_droplet=numpy.mean(bulk_pressure[98:102,0:5])

    return pressure_inside_droplet,pressure_outside_droplet,phase[ydroplet,int(ind_value+ind_value_other)/2],\
           phase[100,1]


def compare_pressures():
    force1=numpy.loadtxt("pressures_Grad-20.txt")
    force5=numpy.loadtxt("pressures_Grad-20_F5.txt")
    
    #force1=force1.reshape(len(force1)/2,2)
    #force5=force5.reshape(len(force5)/2,2)
    pylab.plot([10,10,20,20,30,30,40,40,50,50],force1,'o')
    pylab.plot([10,10,20,20,30,30,40,40,50,50],force5,'s')
    pylab.ylim(ymin=0.0)
    pylab.savefig("pressures_vs_forces.eps")

def initial_pressures():
    #file_list=["vtk0010000_Grad-20_R10_F1.vtk","vtk0010000_Grad-20_R10_F5.vtk",
    #          "vtk0010000_Grad-20_R20_F1.vtk","vtk0010000_Grad-20_R20_F5.vtk",
    #          "vtk0010000_Grad-20_R30_F1.vtk","vtk0010000_Grad-20_R30_F5.vtk",
    #          "vtk0010000_Grad-20_R40_F1.vtk","vtk0010000_Grad-20_R40_F5.vtk",
    #          "vtk0010000_Grad-20_R50_F1.vtk","vtk0010000_Grad-20_R50_F5.vtk"]    		   
    file_list=["vtk0018000_R10_Grad-20_F5.vtk",
               "vtk0018000_R20_Grad-20_F5.vtk",
               "vtk0018000_R30_Grad-20_F5.vtk",
               "vtk0018000_R40_Grad-20_F5.vtk",
               "vtk0018000_R50_Grad-20_F5.vtk"]    		   


    global call_counter
    call_counter=-1
    pressures_in=[]
    pressures_out=[]
    phases_in=[]
    phases_out=[]
    for file_name in file_list:
        pressure_in,pressure_out,phase_in,phase_out=read_all_pressures(file_name)
        pressures_in.append(pressure_in)
        pressures_out.append(pressure_out)
        phases_in.append(phase_in)
        phases_out.append(phase_out)
    
    pressures_in=numpy.array(pressures_in)
    pressures_out=numpy.array(pressures_out)
    #numpy.savetxt("pressures_in.txt",pressures_in)
    #numpy.savetxt("pressures_out.txt",pressures_out)
    #numpy.savetxt("phases_in.txt",phases_in)
    #numpy.savetxt("phases_out.txt",phases_out)
    numpy.savetxt("initial_pressures_before_collision.txt",zip(pressures_in,pressures_out,phases_in,phases_out))
    #pylab.figure(99)
    #legs=[x[11:14] for x in file_list]
    #pylab.savefig("shape_for_grad-20_F5.eps",format="EPS")
    #pylab.savefig("shape_for_grad-20_F5.eps",format="EPS")
    #pylab.legend(legs)
    #pylab.figure(100)
    #pylab.legend(legs)
    # pylab.savefig("velocities_for_grad0.eps",format="EPS")
    pylab.figure(100)
    print pressures_in
    print pressures_out
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    
    pylab.plot(radii,pressures_in,'bs',markersize=8)
    pylab.plot(radii,pressures_out,'bs',markersize=8)
    
    pylab.figure(101)        
    pylab.plot(radii,pressures_in-pressures_out,'bs',markersize=8)
    sigma=numpy.sqrt(aconst*kconst*8.0/9.0)
    
    pylab.plot(radii,sigma*1.0/radii,'r+-')
   

def initial_pressures_read_files():
    
    pressures=numpy.loadtxt("initial_pressures.txt")
    pylab.figure(1)
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    
    pylab.plot(radii,pressures[:,0],'bs',markersize=8)
    pylab.plot(radii,pressures[:,1],'bs',markersize=8)
    
    pylab.figure(2)        
    pylab.plot(radii,pressures[:,0]-pressures[:,1],'bs',markersize=8,markerfacecolor=None)
    sigma=numpy.sqrt(aconst*kconst*8.0/9.0)
    
    # Theoretical pressure
    pylab.plot(radii,sigma*1.0/radii,'r+-')
    # Biased pressure difference
    pylab.plot(radii,pressures[:,0]-1.0/3.0-0.25*aconst,'kd')


def compare():
    global call_counter
    call_counter=-1
    file_list=["vtk0035000_R10_Grad-20_F1.vtk","vtk0036000_R10_Grad-20_F1.vtk",
              "vtk0034000_R20_Grad-20_F1.vtk","vtk0035000_R20_Grad-20_F1.vtk",
              "vtk0033000_R30_Grad-20_F1.vtk","vtk0034000_R30_Grad-20_F1.vtk",
              "vtk0033000_R40_Grad-20_F1.vtk","vtk0034000_R40_Grad-20_F1.vtk",
              "vtk0033000_R50_Grad-20_F1.vtk","vtk0032000_R50_Grad-20_F1.vtk"]    		   
    #file_list=["vtk0020000_R10_Grad-20_F5.vtk","vtk0021000_R10_Grad-20_F5.vtk",
    #           "vtk0020000_R20_Grad-20_F5.vtk","vtk0021000_R20_Grad-20_F5.vtk",
    #           "vtk0020000_R30_Grad-20_F5.vtk","vtk0021000_R30_Grad-20_F5.vtk",
    #           "vtk0020000_R40_Grad-20_F5.vtk","vtk0021000_R40_Grad-20_F5.vtk",
    #           "vtk0020000_R50_Grad-20_F5.vtk","vtk0021000_R50_Grad-20_F5.vtk"]    		   
 
    pressures=[]
    densities=[]
    densities_one=[]
    phases=[]
    for file_name in file_list:
        pressure,density,density_one,phase=get_pressure(file_name)
        pressures.append(pressure)
        densities.append(density)
        densities_one.append(density_one)
        phases.append(phase)
    #numpy.savetxt("pressures_Grad-20_F5.txt",pressures)
    #numpy.savetxt("pressures_Grad-20_another_approach.txt",pressures)
    #numpy.savetxt("densities_Grad-20_F5_another_approach.txt",densities)
    #numpy.savetxt("densities_one_Grad-20_F5_another_approach.txt",densities_one)
    numpy.savetxt("phases_Grad-20_F1_another_approach.txt",phases)
    
    #pylab.figure(99)
    #legs=[x[11:14] for x in file_list]
    #pylab.savefig("shape_for_grad-20_F5.eps",format="EPS")
    #pylab.savefig("shape_for_grad-20_F5.eps",format="EPS")
    #pylab.legend(legs)
    #pylab.figure(100)
    #pylab.legend(legs)
    # pylab.savefig("velocities_for_grad0.eps",format="EPS")
    pylab.figure(102)
    print pressures
    pylab.plot([10,10,20,20,30,30,40,40,50,50],pressures,'bs',markersize=8)
    print numpy.mean(pressures)*numpy.arange(1,5)
    #pylab.savefig("pressure_for_grad-20_F5.eps",format="EPS")
    ##pylab.savefig("pressure_for_grad-20_another_approach.eps",format="EPS")
    pylab.plot([1,2,3,4,5],5*[numpy.mean(pressures)],"r-",linewidth=3)
    pylab.ylim(ymin=0)

def compare_with_initial():
    init_pressures=numpy.loadtxt("initial_pressures.txt")
    init_pressures_before_collision=numpy.loadtxt("initial_pressures_before_collision.txt")
    pressures_F1=numpy.loadtxt("pressures_Grad-20_another_approach.txt")
    pressures_F5=numpy.loadtxt("pressures_Grad-20_F5_another_approach.txt")
    densities_F1=numpy.loadtxt("densities_Grad-20_F1_another_approach.txt")
    densities_F5=numpy.loadtxt("densities_Grad-20_F5_another_approach.txt")
    densities_one_F1=numpy.loadtxt("densities_one_Grad-20_F1_another_approach.txt")
    densities_one_F5=numpy.loadtxt("densities_one_Grad-20_F5_another_approach.txt")
    phases_F1=numpy.loadtxt("phases_Grad-20_F1_another_approach.txt")
    phases_F5=numpy.loadtxt("phases_Grad-20_F5_another_approach.txt")
    
    
    pylab.figure(1)
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    radii2=numpy.array([10,20,30,40,50])
    
    pylab.plot(radii2,pressures_F1[::2],'ko',markersize=8)
    pylab.plot(radii2,pressures_F5[::2],'k^',markersize=8)
    #pylab.plot(radii,init_pressures[:,0]-init_pressures[:,1],'bs',markersize=8,markerfacecolor=None)
    #pylab.plot(radii2,init_pressures_before_collision[:,0]-init_pressures_before_collision[:,1],'kv',markersize=8)
    #pylab.plot(radii,pressures_F5+1.0/3.0-1.0/3.0*densities_F5,'kv',markersize=12)
    sigma=numpy.sqrt(aconst*kconst*8.0/9.0)
    radii_theor=numpy.linspace(5,50,50)
    # Theoretical pressure
    pylab.plot(radii_theor,sigma*1.0/radii_theor,'k-')
    #pylab.plot(radii_theor,sigma*1.0/radii_theor+numpy.mean(densities_one_F5-densities_one_F1)/3.0,'k-.')
    # Biased pressure difference
    #pylab.plot(radii,init_pressures[:,0]-1.0/3.0-0.25*aconst,'kd')
    pylab.legend(["Pressures_F1","Pressures_F5","Theoretical"]) #,"Corrected"])
   
    pylab.xlabel("Radius "+r'''$R$''',fontsize=20)
    pylab.ylabel(r'''$\Delta P$''', fontsize=20)
    pylab.title("Laplace Law", fontsize=30)
    pylab.savefig("comparison_another_approach.eps",dpi=300)
    #pylab.figure(2)
    #pylab.plot(radii,densities_F1,'ko-')
    #pylab.plot(radii,densities_F5,'ks-')
    pylab.figure(3)
    pylab.plot(radii2,densities_one_F1[::2]-1,'ko-')
    pylab.plot(radii2,densities_one_F5[::2]-1,'ks-')
    pylab.xlabel("Radius "+r'''$R$''',fontsize=20)
    pylab.ylabel(r'''$\Delta P_{\mathrm{hydro}}$''', fontsize=20)
    pylab.title("Laplace Law", fontsize=30)
    pylab.legend(["Pressures_F1","Pressures_F5"])
    pylab.savefig("comparison_excess_hydro.eps",dpi=300)
    
    #pylab.figure(4)
    #pylab.plot(radii,phases_F1,'ko-')
    #pylab.plot(radii,phases_F5,'ks-')

def make_nice_graphs():
    file_list=["vtk0035000_R10_Grad-20_F1.vtk","vtk0034000_R20_Grad-20_F1.vtk",
               "vtk0033000_R30_Grad-20_F1.vtk","vtk0033000_R40_Grad-20_F1.vtk",
               "vtk0032000_R50_Grad-20_F1.vtk"]
    file_list=["vtk0020000_R10_Grad-20_F5.vtk","vtk0020000_R20_Grad-20_F5.vtk",
               "vtk0020000_R30_Grad-20_F5.vtk","vtk0020000_R40_Grad-20_F5.vtk",
               "vtk0020000_R50_Grad-20_F5.vtk"]
    #file_list=["vtk0035000_R10_Grad-20_F1.vtk","vtk0036000_R10_Grad-20_F1.vtk",
    #          "vtk0034000_R20_Grad-20_F1.vtk","vtk0035000_R20_Grad-20_F1.vtk",
    #          "vtk0033000_R30_Grad-20_F1.vtk","vtk0034000_R30_Grad-20_F1.vtk",
    #          "vtk0033000_R40_Grad-20_F1.vtk","vtk0034000_R40_Grad-20_F1.vtk",
    #          "vtk0033000_R50_Grad-20_F1.vtk","vtk0032000_R50_Grad-20_F1.vtk"]    		   
    #file_list=["vtk0020000_R10_Grad-20_F5.vtk","vtk0021000_R10_Grad-20_F5.vtk",
    #           "vtk0020000_R20_Grad-20_F5.vtk","vtk0021000_R20_Grad-20_F5.vtk",
    #           "vtk0020000_R30_Grad-20_F5.vtk","vtk0021000_R30_Grad-20_F5.vtk",
    #           "vtk0020000_R40_Grad-20_F5.vtk","vtk0021000_R40_Grad-20_F5.vtk",
    #           "vtk0020000_R50_Grad-20_F5.vtk","vtk0021000_R50_Grad-20_F5.vtk"]    		   

    #styles=['ks','ko','k+','kD','k*','kH','kv','k^','kh','k-']
    
    styles=['k-','k-.','k--','k:','k.','kH','kv','k^','kh','k-']

    for file_counter,file_name in enumerate(file_list):
        phase,density,density_one,velx,vely,dims=read_vtk(file_name)
    
        droplet=numpy.zeros_like(phase)
        positive=numpy.logical_and(phase>=-0.01,phase<1.1)
        droplet[positive]=1
    
        # First figure is to get coordinates
        pylab.figure(1)
        pylab.title("Droplet shape")
        cont=pylab.contour(droplet,levels=[0.0])
        path0=cont.collections[0].get_paths()[0]
        coor_drop=path0.vertices
 
        pylab.figure(2)
        pylab.plot(coor_drop[:,0],coor_drop[:,1],styles[file_counter],linewidth=2,markersize=3)
        
    pylab.figure(2)
    pylab.title("Droplet shapes",fontsize=30)
    pylab.xlim((190,350))
    pylab.ylim((20,180))
    pylab.xlabel(r'''$x$''',fontsize=20)
    pylab.ylabel(r'''$y$''',fontsize=20)
    pylab.legend(["Radius=10","Radius=20","Radius=30","Radius=40","Radius=50"])
    pylab.savefig("shapes_F5_Grad-20.eps")
    
    
if __name__=="__main__":
    #file_name="vtk0018000.vtk"
    #read_vtk(file_name)
    #compare()
    #make_nice_graphs()
    compare_with_initial()
    #compare_pressures()
    #initial_pressures()
    #initial_pressures_read_files()
    pylab.show()

