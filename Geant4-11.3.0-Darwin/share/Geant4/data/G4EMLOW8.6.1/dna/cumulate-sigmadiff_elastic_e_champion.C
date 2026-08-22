{
gROOT->Reset();

Double_t e,trans,angle,d1,d2,d3,d4,d5,max1,max2,max3,max4,max5;
Int_t ncols = 0;
Int_t compt = 0;
Int_t myCompt = 0;
Int_t nbofnrj = 100000;

// 1) LIST OF INCIDENT Energies and bin widths

FILE * fp = fopen("sigmadiff_elastic_e_champion.dat","r");

Double_t tab_e[nbofnrj]=0;
Double_t all_trans[nbofnrj]=0; // angle
Double_t width_e[nbofnrj]=0;
Double_t all_xs1[nbofnrj]=0;
Double_t all_xs2[nbofnrj]=0;
Double_t all_xs3[nbofnrj]=0;
Double_t all_xs4[nbofnrj]=0;
Double_t all_xs5[nbofnrj]=0;

for (Int_t i=0;i<nbofnrj;i++) {tab_e[i]=0; width_e[i]=0; all_xs1[i]=0;all_xs2[i]=0;all_xs3[i]=0;all_xs4[i]=0;all_xs5[i]=0;}

while (1) 
   {
      ncols = fscanf(fp,"%lf %lf %lf",&e,&angle,&d1);
      if (ncols < 0) break;
      
      all_trans[myCompt]=angle;
      
      all_xs1[myCompt]=d1;

      //cout << angle << " " << d1 << endl;

      myCompt++;
            
      if (compt==0) 
      { 
       tab_e[compt]=e; 
      
       //cout << compt << " " << tab_e[0] << endl;
      
       compt=1; 
      }

      if (compt>=1) if (e!=tab_e[compt-1]) 
      { 
        tab_e[compt]=e; 
        
	//cout << compt << " " << tab_e[compt] << endl;
        
	compt++;
      }
      
   }

cout << "Nb of kinetic energies=" << compt << endl;
   
fclose(fp);

for (Int_t i=1;i<nbofnrj;i++)
{
  width_e[i]=all_trans[i]-all_trans[i-1]; 
  if (width_e[i]<0) width_e[i]=0;
  //cout << width_e[i] << endl;
}

//*****************************************************


// 2) SEARCH FOR SUMS (don't forget to multiply by bin width AND sin angle)

Double_t d1cum[compt]=0;

for (Int_t i=0;i<compt;i++) d1cum[i]=0;

FILE * fp = fopen("sigmadiff_elastic_e_champion.dat","r");

Int_t comptbis=0;

myCompt=1;
while (1) 
   {
      ncols = fscanf(fp,"%lf %lf %lf",&e,&angle,&d1);
      if (ncols < 0) break;
      
      if (e==tab_e[comptbis])
      {         
         d1cum[comptbis]=d1cum[comptbis]+
          (all_xs1[myCompt]*std::sin(all_trans[myCompt]*3.141592624/180.)
          +all_xs1[myCompt-1]*std::sin(all_trans[myCompt-1]*3.141592624/180.))
          *0.5*width_e[myCompt];

	/*
        cout 
	<< "--------"
	<< tab_e[comptbis] << " "
	<< comptbis << " " 
	<< d1cum[comptbis] << " " 
	<< angle 
        << endl;
        */

      }

      if (e!=tab_e[comptbis])
      {

	/*
        cout 
	<< "--------"
	<< tab_e[comptbis] << " "
	<< comptbis << " " 
	<< d1cum[comptbis] << " " 
	<< angle
        << endl;
        */

	comptbis++;

        // Starts as zero

        d1cum[comptbis]=d1cum[comptbis]+
         (all_xs1[myCompt]*std::sin(all_trans[myCompt]*3.141592624/180.)
         +all_xs1[myCompt-1]*std::sin(all_trans[myCompt-1]*3.141592624/180.))
         *0.5*width_e[myCompt];
       }
     
      myCompt++;
      
//cout << d1cum[comptbis] << endl;  
}
 
fclose(fp);

// 3) Final cumulated file

remove ("sigmadiff_cumulated_elastic_e_champion_hp.dat");

FILE * fpout = fopen("sigmadiff_cumulated_elastic_e_champion_hp.dat","w");
FILE * fp = fopen("sigmadiff_elastic_e_champion.dat","r");

Int_t comptter = 0;

Double_t sumd1=0;
Double_t tmpd1,tmpd2,tmpd3,tmpd4,tmpd5;

Int_t zerod1=0;

myCompt=0;

while (1) 
   {
      ncols = fscanf(fp,"%lf %lf %lf",&e,&trans,&d1);
      if (ncols < 0) break;
      
      if (e==tab_e[comptter])
      {
        tmpd1=0;

      	if (trans==0)
	{
	  sumd1=0;
	}
	else
        {      
          sumd1=sumd1+(all_xs1[myCompt]*
           std::sin(all_trans[myCompt]*3.141592624/180.)
           +all_xs1[myCompt-1]*std::sin(all_trans[myCompt-1]
             *3.141592624/180.))*0.5*width_e[myCompt];        

          if (d1cum[comptter]!=0) tmpd1= sumd1/d1cum[comptter];
	}

	fprintf (fpout,"%16.9le %16.9le %16.9le\n",e,tmpd1,trans);
		
	//cout << tab_e[comptter] << " " << sumd1 << endl;
	
	//cout << e << " " << trans << " " << tmpd1 << endl;
      }

      if (e!=tab_e[comptter])
      {
	comptter++;

        tmpd1=0;
 
        sumd1=(all_xs1[myCompt]*std::sin(all_trans[myCompt]  
             *3.141592624/180.)+all_xs1[myCompt-1]
             *std::sin(all_trans[myCompt-1]*3.141592624/180.))
             *0.5*width_e[myCompt];        
	
        if (d1cum[comptter]!=0) tmpd1= sumd1/d1cum[comptter];
	
	fprintf (fpout,"%16.9le %16.9le %16.9le\n",e,tmpd1,trans);
      }
      
      myCompt++;
      
   }
fclose(fpout);
fclose(fp);

}
