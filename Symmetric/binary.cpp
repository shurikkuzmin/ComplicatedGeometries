//Simple mass transfer


#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>

//Domain size
int NY;
int NX;
int NUM;

//Other constants
const int NPOP=9;
const int radius=20;
const int radius_droplet=10;
const double wall_gradient=0.0;

//Time steps
int N=100;
int NOUTPUT=10;

//Fields and populations
double *f;
double *f2;
double *g;
double *g2;
double *phi;
double *rho;
double *ux;
double *uy;
int * geometry;

std::vector<int> bb_nodes;
std::vector<char>* dirs;
std::vector<char> main_dir;

//BGK relaxation parameter
double omega=1.0/2.5;

//Underlying lattice parameters
double weights[]={4.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/36.0,1.0/36.0,1.0/36.0,1.0/36.0};
int cx[]={0,1,0,-1,0,1,-1,-1,1};
int cy[]={0,0,1,0,-1,1,1,-1,-1};
int compliment[]={0,3,4,1,2,7,8,5,6};
int symmetricx[NPOP];
int symmetricy[NPOP];
int symmetricxy_left[NPOP];
int symmetricxy_right[NPOP];

void writephase(std::string const & fname)
{

	std::string filename=fname+".dat";
	std::ofstream fout(filename.c_str());
	fout.precision(10);

	for (int iY=0; iY<NY; iY++)
	{
		for (int iX=0; iX<NX; ++iX)	
		{
			int counter=iY*NX+iX;
			fout<<phi[counter]<<" ";
		}
		fout<<"\n";
	}
}

void writegeometry(std::string const & fname)
{
	std::string filename=fname+".dat";
	std::ofstream fout(filename.c_str());
	fout.precision(10);

	for (int iY=0; iY<NY; iY++)
	{
		for (int iX=0; iX<NX; ++iX)	
		{
			int counter=iY*NX+iX;
			fout<<geometry[counter]<<" ";
		}
		fout<<"\n";
	}

}
void writedensity(std::string const & fname)
{
	std::string filename=fname+".dat";
	std::ofstream fout(filename.c_str());
	fout.precision(10);

	for (int iY=0; iY<NY; iY++)
	{
		for (int iX=0; iX<NX; ++iX)	
		{
			int counter=iY*NX+iX;
			fout<<rho[counter]<<" ";
		}
		fout<<"\n";
	}

}

void writevelocityx(std::string const & fname)
{
	std::string filename=fname+".dat";
	std::ofstream fout(filename.c_str());
	fout.precision(10);

	for (int iY=0; iY<NY; iY++)
	{
		for (int iX=0; iX<NX; ++iX)	
		{
			int counter=iY*NX+iX;
			fout<<ux[counter]<<" ";
		}
		fout<<"\n";
	}

}

void writevelocityy(std::string const & fname)
{
	std::string filename=fname+".dat";
	std::ofstream fout(filename.c_str());
	fout.precision(10);

	for (int iY=0; iY<NY; iY++)
	{
		for (int iX=0; iX<NX; ++iX)	
		{
			int counter=iY*NX+iX;
			fout<<uy[counter]<<" ";
		}
		fout<<"\n";
	}

}




void init()
{
	//Creating arrays
	f=new double[NUM*NPOP];
	f2=new double[NUM*NPOP];
	g=new double[NUM*NPOP];
	g2=new double[NUM*NPOP];
	
	//Bulk nodes initialization
	double feq;
	double geq;
	double sum;
	
	for(int iY=0;iY<NY;iY++)
		for(int iX=0;iX<NX;iX++)
		{
			int  counter=iY*NX+iX;
			double dense_temp=rho[counter];
			double ux_temp=ux[counter];
			double uy_temp=uy[counter];
            
            for (int k=0; k<NPOP; k++)
			{
				feq=weights[k]*(dense_temp+3.0*dense_temp*(cx[k]*ux_temp+cy[k]*uy_temp)
								+4.5*dense_temp*((cx[k]*cx[k]-1.0/3.0)*ux_temp*ux_temp
								                +(cy[k]*cy[k]-1.0/3.0)*uy_temp*uy_temp
								                +2.0*ux_temp*uy_temp*cx[k]*cy[k]));
				f[counter*NPOP+k]=feq;
			}
			
		}

	for(int iY=0;iY<NY;iY++)
		for(int iX=0;iX<NX;iX++)
		{
			int  counter=iY*NX+iX;
			double dense_temp=rho[counter];
			double ux_temp=ux[counter];
			double uy_temp=uy[counter];
            
            sum=0;
            for (int k=0; k<NPOP; k++)
				sum+=f[counter*NPOP+k];
			
			rho[counter]=sum;
		}
}

void collide_bulk()
{
    for(int counter=0;counter<NUM;counter++)
    {
		double dense_temp=0.0;
        double phase_temp=0.0;
		double ux_temp=0.0;
		double uy_temp=0.0;
		
		for(int k=0;k<NPOP;k++)
		{
			dense_temp+=f[counter*NPOP+k];
            phase_temp+=g[counter*NPOP+k];
			ux_temp+=f[counter*NPOP+k]*cx[k];
			uy_temp+=f[counter*NPOP+k]*cy[k];
		}
	
		ux_temp=ux_temp/dense_temp;
		uy_temp=uy_temp/dense_temp;
	
		rho[counter]=dense_temp;
		ux[counter]=ux_temp;
		uy[counter]=uy_temp;
        phi[counter]=phase_temp;
        
		double feqeq[NPOP],geqeq[NPOP];

		for (int k=0; k<NPOP; k++)
		{
			feqeq[k]=weights[k]*(dense_temp+3.0*dense_temp*(cx[k]*ux_temp+cy[k]*uy_temp)
            						         +4.5*dense_temp*((cx[k]*cx[k]-1.0/3.0)*ux_temp*ux_temp
															+(cy[k]*cy[k]-1.0/3.0)*uy_temp*uy_temp
					    			                         +2.0*ux_temp*uy_temp*cx[k]*cy[k]));
            geqeq[k]=weights[k]*(phase_temp+3.0*phase_temp*(cx[k]*ux_temp+cy[k]*uy_temp)
                                            +4.5*phase_temp*((cx[k]*cx[k]-1.0/3.0)*ux_temp*ux_temp
                                            +(cy[k]*cy[k]-1.0/3.0)*uy_temp*uy_temp
                                            +2.0*ux_temp*uy_temp*cx[k]*cy[k]));
            
        }
		for(int k=0; k < NPOP; k++)
		{
			f2[counter*NPOP+k]=f[counter*NPOP+k]*(1.0-omega)+omega*feqeq[k];    	
            g2[counter*NPOP+k]=g[counter*NPOP+k]*(1.0-omega)+omega*geqeq[k];
        }
    }

}

void update_bounce_back()
{
	for(int counter=0;counter<bb_nodes.size();counter++)
	{
		
		int dir=main_dir[counter];
		int counter2=bb_nodes[counter]+cy[main_dir[counter]]*NX+cx[main_dir[counter]];
		
		if ( (dir==1) || (dir==3))
			for(int k=0;k<NPOP;k++)
				f2[bb_nodes[counter]*NPOP+k]=f2[counter2*NPOP+symmetricx[k]];
	    
		else if ( (dir==2) || (dir==4))
			for(int k=0;k<NPOP;k++)
				f2[bb_nodes[counter]*NPOP+k]=f2[counter2*NPOP+symmetricy[k]];
		else if ( (dir==5) || (dir==7))
			for(int k=0;k<NPOP;k++)
				f2[bb_nodes[counter]*NPOP+k]=f2[counter2*NPOP+symmetricxy_right[k]];
		else 
			for(int k=0;k<NPOP;k++)
				f2[bb_nodes[counter]*NPOP+k]=f2[counter2*NPOP+symmetricxy_left[k]];

		//density and velocity specification
		
		double dense_temp=0.0;
		double ux_temp=0.0;
		double uy_temp=0.0;
		
		for(int k=0;k<NPOP;k++)
		{
			dense_temp=dense_temp+f2[bb_nodes[counter]*NPOP+k];
			ux_temp=ux_temp+f2[bb_nodes[counter]*NPOP+k]*cx[k];
			uy_temp=uy_temp+f2[bb_nodes[counter]*NPOP+k]*cy[k];
		}
		ux_temp=ux_temp/dense_temp;
		uy_temp=uy_temp/dense_temp;
		
		rho[bb_nodes[counter]]=dense_temp;
		ux[bb_nodes[counter]]=ux_temp;
		uy[bb_nodes[counter]]=uy_temp;
	}
	
}

void update_phase()
{
	for(int counter=0;counter<bb_nodes.size();counter++)
	{
		int dir=main_dir[counter];
		int counter2=bb_nodes[counter]+cy[main_dir[counter]]*NX+cx[main_dir[counter]];
		phi[bb_nodes[counter]]=phi[bb_nodes[counter2]]+wall_gradient;
	}
	
}



void initialize_geometry()
{
	NY=201;
	NX=201;
	NUM=NX*NY;
    geometry=new int[NUM];
    rho=new double[NUM];
    ux=new double[NUM];
    uy=new double[NUM];
    phi=new double[NUM];
    

	//Solid nodes 
	for(int counter=0;counter<NUM;counter++)
	{
		int iX=counter%NX;
		int iY=counter/NX;
	    
	    if ((iX-(NX-1)/2)*(iX-(NX-1)/2)+(iY-(NY-1)/2)*(iY-(NY-1)/2)<radius*radius)
	    	geometry[counter]=-1;
	    else
	    	geometry[counter]=1;  
	}

	for(int counter=0;counter<NUM;counter++)
	{
	    bool flag=false;
	    if (geometry[counter]==-1)
	    {
	    	int iX=counter%NX;
	    	int iY=counter/NX;
	    	for (int iPop=1;iPop<NPOP;iPop++)
	    	{
				int iX2=(iX+cx[iPop]+NX)%NX;
			 	int iY2=(iY+cy[iPop]+NY)%NY;
	    		int counter2=iY2*NX+iX2;
	    		if (geometry[counter2]==1)
	    			flag=true;
	    	}
	    }
	    if (flag)
	    	geometry[counter]=0;
	}

	//Initialization of density
    for(int counter=0;counter<NUM;counter++)
    {
		ux[counter]=0.0;
		uy[counter]=0.0;

		if (geometry[counter]==0)
		{
		    rho[counter]=1.0;
			bb_nodes.push_back(counter);
		}
		else if(geometry[counter]==-1)
			rho[counter]=-1.0;
		else
			rho[counter]=1.0;
	}
	
	//Identifying fluids
	for(int counter=0;counter<NUM;counter++)
	{
		int iX=counter%NX;
		int iY=counter/NX;
		
		if ((iX-(NX-1)/2)*(iX-(NX-1)/2)+(iY-(NY-1)/2-(radius+radius_droplet))*(iY-(NY-1)/2-(radius+radius_droplet))<radius_droplet*radius_droplet)
		    phi[counter]=1.0;
		else
			phi[counter]=-1.0;
	}
	
	symmetricx[0]=0;
    for(int k=1;k<NPOP;k++)
    	for(int l=1;l<NPOP;l++)
    	    if ((-cx[k]==cx[l])&&(cy[k]==cy[l]))
            {
                symmetricx[k]=l;
                break;
            }
    
     symmetricy[0]=0;
     for(int k=1;k<NPOP;k++)
        for(int l=1;l<NPOP;l++)
            if ((cx[k]==cx[l])&&(cy[k]==-cy[l]))
            {
           		symmetricy[k]=l;
                break;
            }
     
     symmetricxy_left[0]=0;
     symmetricxy_left[1]=2;
     symmetricxy_left[2]=1;
     symmetricxy_left[3]=4;
     symmetricxy_left[4]=3;
     symmetricxy_left[5]=5;
     symmetricxy_left[6]=8;
     symmetricxy_left[7]=7;
     symmetricxy_left[8]=6;
           
     symmetricxy_right[0]=0;
     symmetricxy_right[1]=4;
     symmetricxy_right[2]=3;
     symmetricxy_right[3]=2;
     symmetricxy_right[4]=1;
     symmetricxy_right[5]=7;
     symmetricxy_right[6]=6;
     symmetricxy_right[7]=5;
     symmetricxy_right[8]=8;

     
	//Finding directions for BB nodes
    dirs=new std::vector<char>[bb_nodes.size()];
    for(int counter=0;counter<bb_nodes.size();counter++)
	{
		for(int k=1;k<NPOP;k++)
		{
			int counter2=bb_nodes[counter]+cy[k]*NX+cx[k];
			if (geometry[counter2]==1)
				dirs[counter].push_back(k);
		}
	}
	

	for(int counter=0;counter<bb_nodes.size();counter++)
	{
     	int nx=0;
     	int ny=0;
		bool flag=false;
     	for(int k=1;k<5;k++)
		{
			int counter2=bb_nodes[counter]+cy[k]*NX+cx[k];
			if (geometry[counter2]==1)
			{
				flag=true;
				nx=nx+cx[k];
				ny=ny+cy[k];
			}
			
		}
		if (!flag)
			for(int k=5;k<NPOP;k++)
			{
				int counter2=bb_nodes[counter]+cy[k]*NX+cx[k];
				if (geometry[counter2]==1)
				{
					flag=true;
					nx=nx+cx[k];
					ny=ny+cy[k];
				}
			}
		
		for(int k=1;k<NPOP;k++)
			if ((nx==cx[k])&&(ny==cy[k]))
			{
				main_dir.push_back(k);
			}
			
	}
	std::cout<<"BB size="<<bb_nodes.size()<<"\n";
	std::cout<<"Main size="<<main_dir.size()<<"\n";
	writephase("phase");
	writegeometry("geometry");
}


void finish_simulation()
{
	delete[] geometry;
	delete[] rho;
	delete[] ux;
	delete[] uy;
	delete[] f;
	delete[] f2;
	delete[] dirs;
	delete[] phi;
	delete[] g;
	delete[] g2;
}

void stream()
{
    for(int counter=0;counter<NUM;counter++)
	{
		int iX=counter%NX;
		int iY=counter/NX;

		for(int iPop=0;iPop<NPOP;iPop++)
		{
			int iX2=(iX-cx[iPop]+NX)%NX;
			int iY2=(iY-cy[iPop]+NY)%NY;
			int counter2=iY2*NX+iX2;
			f[counter*NPOP+iPop]=f2[counter2*NPOP+iPop];
			g[counter*NPOP+iPop]=g2[counter2*NPOP+iPop];
		}
	}

	
}


int main(int argc, char* argv[])
{

    initialize_geometry();
    init();
      

	for(int counter=0;counter<=N;counter++)
	{
        update_phase();
        collide_bulk();
        update_bounce_back();
		stream();
        
		//Writing files
		if (counter%NOUTPUT==0)
		{
			std::cout<<"Counter="<<counter<<"\n";
  			std::stringstream filewritedensity;
  			std::stringstream filewritevelocityx;
  			std::stringstream filewritevelocityy;
 			
 			std::stringstream counterconvert;
 			counterconvert<<counter;
 			filewritedensity<<std::fixed;
 			filewritevelocityx<<std::fixed;
 			filewritevelocityy<<std::fixed;

			filewritedensity<<"den"<<std::string(7-counterconvert.str().size(),'0')<<counter;
			filewritevelocityx<<"velx"<<std::string(7-counterconvert.str().size(),'0')<<counter;
			filewritevelocityy<<"vely"<<std::string(7-counterconvert.str().size(),'0')<<counter;
			
 			writedensity(filewritedensity.str());
 			writevelocityx(filewritevelocityx.str());
 			writevelocityy(filewritevelocityy.str());
		}

	}

    finish_simulation();
   
   	return 0;
}
