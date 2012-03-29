import numpy
import pylab

def show_results():
    gradients=numpy.linspace(-0.4,0.4,9)
    forces=numpy.linspace(0.000001,0.000005,5)
    pylab.interactive(False)
    # Tags for results
    # 1 stays for 1 droplet attached front
    # 2 stays for 1 droplet attached back
    # 3 stays for 2 droplets attached back
    # 4 stays for not attached
    # 5 stays for breakup to 2 droplets
    # 6 stays for breakup with coalescense
    
    visc1=numpy.array([[1,2,2,2,2],
                       [1,2,2,2,2],
                       [1,3,2,2,2],
                       [1,3,3,3,3],
                       [1,3,3,3,3],
                       [1,3,3,3,3],
                       [4,4,3,3,5],
                       [4,4,5,5,5],
                       [4,5,5,5,5]])

    visc3=numpy.array([[1,2,2,2,2],
                       [1,2,2,2,2],
                       [1,2,2,2,2],
                       [1,2,2,2,2],
                       [1,3,3,3,2],
                       [1,3,3,3,3],
                       [1,3,3,3,5],
                       [4,4,5,5,5],
                       [4,4,5,5,5]])
                       
    visc5=numpy.array([[2,2,2,2,2],
                       [1,2,2,2,2],
                       [1,2,2,2,2],
                       [1,3,2,2,2],
                       [1,3,3,2,2],
                       [1,3,3,3,3],
                       [1,3,3,3,5],
                       [4,4,5,5,5],
                       [4,4,5,5,5]])

    visc10=numpy.array([[1,2,2,2,2],
                        [1,2,2,2,2],
                        [1,3,2,2,2],
                        [1,3,2,2,2],
                        [1,3,2,2,2],
                        [1,3,3,3,3],
                        [1,3,3,3,3],
                        [4,4,3,3,5],
                        [4,4,5,5,5]])
    
    pylab.figure(figsize=(15,15))
    pylab.subplot(221)
    pylab.title("Viscosity ratio=1")
    pylab.imshow(visc1.transpose(),origin="lower") #,extent=[gradients[0],gradients[-1],forces[0],forces[-1]])
    pylab.colorbar()                   

    pylab.subplot(222)
    pylab.title("Viscosity ratio=3")
    pylab.imshow(visc3.transpose(),origin="lower") #,interpolation="none") #extent=[gradients[0],gradients[-1],forces[0],forces[-1]])
    pylab.colorbar()                   

    pylab.subplot(223)
    pylab.title("Viscosity ratio=5")
    pylab.imshow(visc5.transpose(),origin="lower") #,interpolation="none")
    pylab.colorbar()                   

    pylab.subplot(224)
    pylab.title("Viscosity ratio=10")
    pylab.imshow(visc10.transpose(),origin="lower") #,interpolation="none")
    pylab.colorbar()               
        
    pylab.savefig("results_map.png",dpi=300)             
    
if __name__=="__main__":
    show_results()
    pylab.show()