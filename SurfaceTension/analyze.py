import numpy
import vtk
import pylab
def read_vtk(file_name):
        
    #constants of binary liquid model
    #global call_counter
    #styles=['ks','ks','k+','k+','ko','ko','kv','kv']
    #styles=['ks','ko','k+','kD','k*','kH','kv','k^','kh','k-']

    #call_counter=call_counter+1
    #print call_counter
    
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
    return phase,density,density_one,dims
    
def get_droplet(file_name,surface_tension_ratio):
    phase,density,density_one,dims=read_vtk(file_name)

    aconst=0.04*surface_tension_ratio
    kconst=0.04*surface_tension_ratio
    
    droplet=numpy.zeros_like(phase)
    positive=numpy.logical_and(phase>=-0.01,phase<1.1)
    droplet[positive]=1
    
    pylab.figure(1)
    pylab.title("Droplet shape")
    cont=pylab.contour(droplet,levels=[0.0])
    
    pylab.figure(2)
    path0=cont.collections[0].get_paths()[0]
    coor_drop=path0.vertices
    pylab.plot(coor_drop[:,0],coor_drop[:,1],markersize=5,markerfacecolor="None")
    #get the largest coordinate and start counting from it
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
    print "Ind=",ind
    print "Ind_other=",ind_other
    print "Ind value=",ind_value
    print "Ind value ohter=",ind_value_other
    y=coor_drop[:,1]
    x=coor_drop[:,0]
    x=numpy.roll(x,-ind)
    y=numpy.roll(y,-ind)    
    #velx_circle=numpy.roll(velx_circle,-ind) 
    #pylab.figure(100)
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
    #pressure difference -if bubble is not nice
    pressure_difference_bad=bulk_pressure[ydroplet,int(ind_value+ind_value_other)/2]\
                           -1.0/3.0-aconst*0.25
    print "x,y=",xdroplet,ydroplet
    print "Pressure difference bad=",pressure_difference_bad
    print "Index=",int(ind+ind_other)/2
    return pressure_difference_bad,density[ydroplet,int(ind_value+ind_value_other)/2],\
           density_one[ydroplet,int(ind_value+ind_value_other)/2]

def compare():
    #ratio04_begin=["vtk0010000_R10_Grad-20_F1_Ratio04.vtk","vtk0010000_R10_Grad-20_F1_Ratio04.vtk",
    #         "vtk0010000_R20_Grad-20_F1_Ratio04.vtk","vtk0010000_R20_Grad-20_F1_Ratio04.vtk",
    #         "vtk0010000_R30_Grad-20_F1_Ratio04.vtk","vtk0010000_R30_Grad-20_F1_Ratio04.vtk",
    #         "vtk0010000_R40_Grad-20_F1_Ratio04.vtk","vtk0010000_R40_Grad-20_F1_Ratio04.vtk",
    #         "vtk0010000_R50_Grad-20_F1_Ratio04.vtk","vtk0010000_R50_Grad-20_F1_Ratio04.vtk"]
    #ratio04=["vtk0036000_R10_Grad-20_F1_Ratio04.vtk","vtk0037000_R10_Grad-20_F1_Ratio04.vtk",
    #         "vtk0035000_R20_Grad-20_F1_Ratio04.vtk","vtk0036000_R20_Grad-20_F1_Ratio04.vtk",
    #         "vtk0035000_R30_Grad-20_F1_Ratio04.vtk","vtk0036000_R30_Grad-20_F1_Ratio04.vtk",
    #         "vtk0035000_R40_Grad-20_F1_Ratio04.vtk","vtk0036000_R40_Grad-20_F1_Ratio04.vtk",
    #         "vtk0035000_R50_Grad-20_F1_Ratio04.vtk","vtk0036000_R50_Grad-20_F1_Ratio04.vtk"]
    #ratio07=["vtk0035000_R10_Grad-20_F1_Ratio07.vtk","vtk0036000_R10_Grad-20_F1_Ratio07.vtk",
    #         "vtk0034000_R20_Grad-20_F1_Ratio07.vtk","vtk0035000_R20_Grad-20_F1_Ratio07.vtk",
    #         "vtk0034000_R30_Grad-20_F1_Ratio07.vtk","vtk0035000_R30_Grad-20_F1_Ratio07.vtk",
    #         "vtk0033000_R40_Grad-20_F1_Ratio07.vtk","vtk0034000_R40_Grad-20_F1_Ratio07.vtk",
    #         "vtk0033000_R50_Grad-20_F1_Ratio07.vtk","vtk0034000_R50_Grad-20_F1_Ratio07.vtk"]
    #ratio13=["vtk0035000_R10_Grad-20_F1_Ratio13.vtk","vtk0036000_R10_Grad-20_F1_Ratio13.vtk",
    #         "vtk0034000_R20_Grad-20_F1_Ratio13.vtk","vtk0035000_R20_Grad-20_F1_Ratio13.vtk",
    #         "vtk0033000_R30_Grad-20_F1_Ratio13.vtk","vtk0034000_R30_Grad-20_F1_Ratio13.vtk",	
    #         "vtk0032000_R40_Grad-20_F1_Ratio13.vtk","vtk0033000_R40_Grad-20_F1_Ratio13.vtk",
    #         "vtk0032000_R50_Grad-20_F1_Ratio13.vtk","vtk0033000_R50_Grad-20_F1_Ratio13.vtk"]	
    ratio16=["vtk0035000_R10_Grad-20_F1_Ratio16.vtk","vtk0036000_R10_Grad-20_F1_Ratio16.vtk",
             "vtk0034000_R20_Grad-20_F1_Ratio16.vtk","vtk0035000_R20_Grad-20_F1_Ratio16.vtk",
             "vtk0033000_R30_Grad-20_F1_Ratio16.vtk","vtk0034000_R30_Grad-20_F1_Ratio16.vtk",
             "vtk0032000_R40_Grad-20_F1_Ratio16.vtk","vtk0033000_R40_Grad-20_F1_Ratio16.vtk",
	         "vtk0032000_R50_Grad-20_F1_Ratio16.vtk","vtk0033000_R50_Grad-20_F1_Ratio16.vtk"]	   		   
 
    file_list=ratio16
    ending="ratio16"
    pressures=[]
    densities=[]
    densities_one=[]
    for file_name in file_list:
        pressure,density,density_one=get_droplet(file_name,0.4)
        pressures.append(pressure)
        densities.append(density)
        densities_one.append(density_one)
        
    numpy.savetxt("pressures_Grad-20_F1_"+ending+".txt",pressures)
    numpy.savetxt("densities_Grad-20_F1_"+ending+".txt",densities)
    numpy.savetxt("densities_one_Grad-20_F1_"+ending+".txt",densities_one)
    
    pylab.figure(99)
    legs=[x[11:14] for x in file_list]
    pylab.savefig("shape_for_grad-20_F1_"+ending+".eps",format="EPS")
    #pylab.legend(legs)
    pylab.figure(100)
    #pylab.legend(legs)
    # pylab.savefig("velocities_for_grad0.eps",format="EPS")
    pylab.figure(102)
    print pressures
    pylab.plot([10,10,20,20,30,30,40,40,50,50],pressures,'bs',markersize=8)
    print numpy.mean(pressures)
    pylab.savefig("pressure_for_grad-20_"+ending+".eps",format="EPS")
    pylab.plot([10,20,30,40,50],5*[numpy.mean(pressures)],"r-",linewidth=3)
    pylab.ylim(ymin=0)

def compare_F5():
    #ratio04=["vtk021000_R10_F5_R04.vtk","vtk022000_R10_F5_R04.vtk",
    #         "vtk020000_R20_F5_R04.vtk","vtk021000_R20_F5_R04.vtk",
    #         "vtk020000_R30_F5_R04.vtk","vtk021000_R30_F5_R04.vtk",
    #         "vtk021000_R40_F5_R04.vtk","vtk022000_R40_F5_R04.vtk",
    #         "vtk021000_R50_F5_R04.vtk","vtk022000_R50_F5_R04.vtk"]
    #ratio07=["vtk020000_R10_F5_R07.vtk","vtk021000_R10_F5_R07.vtk",
    #         "vtk020000_R20_F5_R07.vtk","vtk021000_R20_F5_R07.vtk",
    #         "vtk020000_R30_F5_R07.vtk","vtk021000_R30_F5_R07.vtk",
    #         "vtk020000_R40_F5_R07.vtk","vtk021000_R40_F5_R07.vtk",
    #         "vtk020000_R50_F5_R07.vtk","vtk021000_R50_F5_R07.vtk"]
    ratio13=["vtk020000_R10_F5_R13.vtk","vtk021000_R10_F5_R13.vtk",
             "vtk019000_R20_F5_R13.vtk","vtk020000_R20_F5_R13.vtk",
             "vtk019000_R30_F5_R13.vtk","vtk020000_R30_F5_R13.vtk",
             "vtk019000_R40_F5_R13.vtk","vtk020000_R40_F5_R13.vtk",
             "vtk019000_R50_F5_R13.vtk","vtk020000_R50_F5_R13.vtk"]
             
 
    file_list=ratio13
    ending="ratio13"
    pressures=[]
    densities=[]
    densities_one=[]
    for file_name in file_list:
        pressure,density,density_one=get_droplet("Force5/"+file_name,0.4)
        pressures.append(pressure)
        densities.append(density)
        densities_one.append(density_one)
        
    numpy.savetxt("pressures_Grad-20_F5_"+ending+".txt",pressures)
    numpy.savetxt("densities_Grad-20_F5_"+ending+".txt",densities)
    numpy.savetxt("densities_one_Grad-20_F5_"+ending+".txt",densities_one)
    
    pylab.figure(99)
    legs=[x[11:14] for x in file_list]
    pylab.savefig("shape_for_grad-20_F5_"+ending+".eps",format="EPS")
    #pylab.legend(legs)
    pylab.figure(100)
    #pylab.legend(legs)
    # pylab.savefig("velocities_for_grad0.eps",format="EPS")
    pylab.figure(102)
    print pressures
    pylab.plot([10,10,20,20,30,30,40,40,50,50],pressures,'bs',markersize=8)
    print numpy.mean(pressures)
    pylab.savefig("pressure_for_grad-20_"+ending+".eps",format="EPS")
    pylab.plot([10,20,30,40,50],5*[numpy.mean(pressures)],"r-",linewidth=3)
    pylab.ylim(ymin=0)


def compare_pressures():
    pressures_F1_ratio_04=numpy.loadtxt("pressures_Grad-20_F1_ratio04.txt")
    pressures_F1_ratio_07=numpy.loadtxt("pressures_Grad-20_F1_ratio07.txt")
    pressures_F1_ratio_13=numpy.loadtxt("pressures_Grad-20_F1_ratio13.txt")
    pressures_F1_ratio_16=numpy.loadtxt("pressures_Grad-20_F1_ratio16.txt")
    
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    radii2=numpy.array([10,20,30,40,50])
    pylab.plot(radii2,pressures_F1_ratio_04[1::2],'ko')
    pylab.plot(radii2,pressures_F1_ratio_07[::2],'ks')
    pylab.plot(radii2,pressures_F1_ratio_13[::2],'k^')
    pylab.plot(radii2,pressures_F1_ratio_16[1::2],'kv')
    sigma_04=numpy.sqrt(8.0/9.0*0.04*0.04)*0.4
    sigma_07=numpy.sqrt(8.0/9.0*0.04*0.04)*0.7
    sigma_13=numpy.sqrt(8.0/9.0*0.04*0.04)*1.3
    sigma_16=numpy.sqrt(8.0/9.0*0.04*0.04)*1.6
    radii_theor=numpy.linspace(5,50,50)
    pylab.plot(radii_theor,sigma_04/radii_theor,'k-')
    pylab.plot(radii_theor,sigma_07/radii_theor,'k--')
    pylab.plot(radii_theor,sigma_13/radii_theor,'k-.')
    pylab.plot(radii_theor,sigma_16/radii_theor,'k:')
        
    pylab.legend(["Ratio=0.4","Ratio=0.7","Ratio=1.3","Ratio=1.6",\
                  "Theor=0.4","Theor=0.7","Theor=1.3","Theor=1.6"])
    pylab.xlim(xmin=8)
    pylab.ylim(ymin=0.0)
    pylab.xlabel("Radius R",fontsize=20)
    pylab.ylabel(r'''$\Delta P$''',fontsize=20)
    pylab.title("Surface tension ratio",fontsize=30)
    pylab.savefig("pressures_vs_surface_tension_F1.eps")

def compare_pressures_F5():
    pressures_F5_ratio_04=numpy.loadtxt("pressures_Grad-20_F5_ratio04.txt")
    pressures_F5_ratio_07=numpy.loadtxt("pressures_Grad-20_F5_ratio07.txt")
    pressures_F5_ratio_13=numpy.loadtxt("pressures_Grad-20_F5_ratio13.txt")
    
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    radii2=numpy.array([10,20,30,40,50])
    pylab.plot(radii2,pressures_F5_ratio_04[::2],'ko')
    pylab.plot(radii2,pressures_F5_ratio_07[::2],'ks')
    pylab.plot(radii2,pressures_F5_ratio_13[1::2],'k^')
    sigma_04=numpy.sqrt(8.0/9.0*0.04*0.04)*0.4
    sigma_07=numpy.sqrt(8.0/9.0*0.04*0.04)*0.7
    sigma_13=numpy.sqrt(8.0/9.0*0.04*0.04)*1.3
    radii_theor=numpy.linspace(5,50,50)
    pylab.plot(radii_theor,sigma_04/radii_theor,'k-')
    pylab.plot(radii_theor,sigma_07/radii_theor,'k--')
    pylab.plot(radii_theor,sigma_13/radii_theor,'k-.')
        
    pylab.legend(["Ratio=0.4","Ratio=0.7","Ratio=1.3",\
                  "Theor=0.4","Theor=0.7","Theor=1.3"])
    pylab.xlim(xmin=8)
    pylab.ylim(ymin=0.0)
    pylab.xlabel("Radius R",fontsize=20)
    pylab.ylabel(r'''$\Delta P$''',fontsize=20)
    pylab.title("Surface tension ratio",fontsize=30)
    pylab.savefig("pressures_vs_surface_tension_F5.eps")

def compare_F1_and_F5():
    pressures_F1_ratio_04=numpy.loadtxt("pressures_Grad-20_F1_ratio04.txt")
    pressures_F1_ratio_07=numpy.loadtxt("pressures_Grad-20_F1_ratio07.txt")
    pressures_F1_ratio_13=numpy.loadtxt("pressures_Grad-20_F1_ratio13.txt")
    pressures_F5_ratio_04=numpy.loadtxt("pressures_Grad-20_F5_ratio04.txt")
    pressures_F5_ratio_07=numpy.loadtxt("pressures_Grad-20_F5_ratio07.txt")
    pressures_F5_ratio_13=numpy.loadtxt("pressures_Grad-20_F5_ratio13.txt")
    
    radii=numpy.array([10,10,20,20,30,30,40,40,50,50])
    radii2=numpy.array([10,20,30,40,50])
    pylab.plot(radii2,pressures_F1_ratio_04[1::2],'ko')
    pylab.plot(radii2,pressures_F1_ratio_07[::2],'ks')
    pylab.plot(radii2,pressures_F1_ratio_13[::2],'k^')
    pylab.plot(radii2,pressures_F5_ratio_04[::2],'ko',markerfacecolor="None")
    pylab.plot(radii2,pressures_F5_ratio_07[::2],'ks',markerfacecolor="None")
    pylab.plot(radii2,pressures_F5_ratio_13[1::2],'k^',markerfacecolor="None")
    sigma_04=numpy.sqrt(8.0/9.0*0.04*0.04)*0.4
    sigma_07=numpy.sqrt(8.0/9.0*0.04*0.04)*0.7
    sigma_13=numpy.sqrt(8.0/9.0*0.04*0.04)*1.3
    radii_theor=numpy.linspace(5,50,50)
    pylab.plot(radii_theor,sigma_04/radii_theor,'k-')
    pylab.plot(radii_theor,sigma_07/radii_theor,'k--')
    pylab.plot(radii_theor,sigma_13/radii_theor,'k-.')
        
    pylab.legend(["Ratio=0.4","Ratio=0.7","Ratio=1.3",\
                  "Ratio_F5=0.4","Ratio_F5=0.7","Ratio_F5=1.3",\
                  "Theor=0.4","Theor=0.7","Theor=1.3"])
    pylab.xlim(xmin=8)
    pylab.ylim(ymin=0.0)
    pylab.xlabel("Radius R",fontsize=20)
    pylab.ylabel(r'''$\Delta P$''',fontsize=20)
    pylab.title("Surface tension ratio",fontsize=30)
    pylab.savefig("p_vs_s_F1_F5.eps")



if __name__=="__main__":
    #file_name="vtk0018000.vtk"
    #read_vtk(file_name)
    #compare()
    #compare_F5()
    #compare_pressures()
    #compare_pressures_F5()
    compare_F1_and_F5()
    pylab.show()

