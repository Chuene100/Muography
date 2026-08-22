{

gROOT->Reset();


Float_t e,trans,d1,d2,d3,d4,d5,max1,max2,max3,max4,max5;
Int_t ncols = 0;
Int_t compt = 0;
Int_t myCompt = 0;
Int_t nbofnrj = 10000;

// 1) LIST OF INCIDENT Energies and bin widths

FILE * fp = fopen("new_sigmadiff_ionisation_e_born.dat","r");

Float_t tab_e[nbofnrj]=0;
Float_t all_trans[nbofnrj]=0;
Float_t width_e[nbofnrj]=0;
Float_t all_xs1[nbofnrj]=0;
Float_t all_xs2[nbofnrj]=0;
Float_t all_xs3[nbofnrj]=0;
Float_t all_xs4[nbofnrj]=0;
Float_t all_xs5[nbofnrj]=0;

for (Int_t i=0;i<nbofnrj;i++) {tab_e[i]=0; width_e[i]=0; all_xs1[i]=0;all_xs2[i]=0;all_xs3[i]=0;all_xs4[i]=0;all_xs5[i]=0;}

while (1) 
   {
      ncols = fscanf(fp,"%f %f %f %f %f %f %f",&e,&trans,&d1,&d2,&d3,&d4,&d5);
      if (ncols < 0) break;
      
      all_trans[myCompt]=trans;
      
      all_xs1[myCompt]=d1;
      all_xs2[myCompt]=d2;
      all_xs3[myCompt]=d3;
      all_xs4[myCompt]=d4;
      all_xs5[myCompt]=d5;

      myCompt++;
      
      if (compt==0) 
      { 
       tab_e[compt]=e; 
      
       /*cout << compt << " " << tab_e[0] << endl;*/
      
       compt=1; 
      }

      if (compt>=1) if (e!=tab_e[compt-1]) 
      { 
        tab_e[compt]=e; 
        
	//cout << compt << " " << tab_e[compt] << endl;
        
	compt++;
	}
      
   }

//cout << compt << endl;
   
fclose(fp);

for (Int_t i=1;i<nbofnrj;i++) 
{
  width_e[i]=all_trans[i]-all_trans[i-1]; 
  if (width_e[i]<0) width_e[i]=0;
  //cout << width_e[i] << endl; 
}

// 2) SEARCH FOR SUMS (don't forget to multiply by bin width)

Float_t d1cum[compt]=0;
Float_t d2cum[compt]=0;
Float_t d3cum[compt]=0;
Float_t d4cum[compt]=0;
Float_t d5cum[compt]=0;

for (Int_t i=0;i<compt;i++) d1cum[i]=0;
for (Int_t i=0;i<compt;i++) d2cum[i]=0;
for (Int_t i=0;i<compt;i++) d3cum[i]=0;
for (Int_t i=0;i<compt;i++) d4cum[i]=0;
for (Int_t i=0;i<compt;i++) d5cum[i]=0;

FILE * fp = fopen("new_sigmadiff_ionisation_e_born.dat","r");

Int_t comptbis=0;

// WE DO NOT CUMULATE DXS VALUES FOR ETRANSF < IONIZATION LEVEL ENERGIES

myCompt=0;
while (1) 
   {
      ncols = fscanf(fp,"%f %f %f %f %f %f %f",&e,&trans,&d1,&d2,&d3,&d4,&d5);
      if (ncols < 0) break;
      
      if (e==tab_e[comptbis])
      {
         
	 // Note that max* are the maximum energy transfers including secondry kinetic energy AND medium transfer
	 // This is different from the proton macro case for which the max* are ONLY for the secondary kinetic
	 
         if ((e+10.79)/2. > e) max1=e;
         else max1 = (e+10.79)/2.;
	 
         if ((e+13.39)/2. > e) max2=e;
         else max2 = (e+13.39)/2.;
	 
         if ((e+16.05)/2. > e) max3=e;
         else max3 = (e+16.05)/2.;
	 	 
         if ((e+32.30)/2. > e) max4=e;
         else max4 = (e+32.30)/2.;
	 
         if ((e+539.)/2. > e) max5=e;
         else max5 = (e+539.)/2.;	 
	 
	 if (trans>=10.79&&trans<=max1) d1cum[comptbis]=d1cum[comptbis]+(all_xs1[myCompt]+all_xs1[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=13.39&&trans<=max2) d2cum[comptbis]=d2cum[comptbis]+(all_xs2[myCompt]+all_xs2[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=16.05&&trans<=max3) d3cum[comptbis]=d3cum[comptbis]+(all_xs3[myCompt]+all_xs3[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=32.30&&trans<=max4) d4cum[comptbis]=d4cum[comptbis]+(all_xs4[myCompt]+all_xs4[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=539.0&&trans<=max5) d5cum[comptbis]=d5cum[comptbis]+(all_xs5[myCompt]+all_xs5[myCompt-1])*0.5*width_e[myCompt];
	
	 
	 /*
	 if (comptbis>1) cout << comptbis << " " << e << " trans=" << trans << " myCompt=" << myCompt << " " << all_xs3[myCompt] << " " 
	  << all_xs3[myCompt-1] << " " 
	  << (all_xs3[myCompt]+all_xs3[myCompt-1])*0.5*width_e[myCompt] << " " << d3cum[comptbis] << " " << max3 << endl;
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
	<< d2cum[comptbis] << " " 
	<< d3cum[comptbis] << " " 
	<< d4cum[comptbis] << " " 
	<< d5cum[comptbis] << " " 
	<< endl;
       */ 

	comptbis++;

         if ((e+10.79)/2. > e) max1=e;
         else max1 = (e+10.79)/2.;
	 
         if ((e+13.39)/2. > e) max2=e;
         else max2 = (e+13.39)/2.;
	 
         if ((e+16.05)/2. > e) max3=e;
         else max3 = (e+16.05)/2.;
	 
         if ((e+32.30)/2. > e) max4=e;
         else max4 = (e+32.30)/2.;
	 
         if ((e+539.)/2. > e) max5=e;
         else max5 = (e+539.)/2.;	 
	 
         if (trans>=10.79&&trans<=max1) d1cum[comptbis]=(all_xs1[myCompt]+all_xs1[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=13.39&&trans<=max2) d2cum[comptbis]=(all_xs2[myCompt]+all_xs2[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=16.05&&trans<=max3) d3cum[comptbis]=(all_xs3[myCompt]+all_xs3[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=32.30&&trans<=max4) d4cum[comptbis]=(all_xs4[myCompt]+all_xs4[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=539.0&&trans<=max5) d5cum[comptbis]=(all_xs5[myCompt]+all_xs5[myCompt-1])*0.5*width_e[myCompt];
      }
      
      myCompt++;
      
   }
//cout << comptbis << endl;   
fclose(fp);

// 3) Final cumulated file

remove ("new_sigmadiff_cumulated_ionisation_e_born.dat");

FILE * fpout = fopen("new_sigmadiff_cumulated_ionisation_e_born.dat","w");
FILE * fp = fopen("new_sigmadiff_ionisation_e_born.dat","r");

Int_t comptter = 0;

Float_t sumd1=0;
Float_t sumd2=0;
Float_t sumd3=0;
Float_t sumd4=0;
Float_t sumd5=0;

Float_t tmpd1,tmpd2,tmpd3,tmpd4,tmpd5;

Int_t zerod1=0;
Int_t zerod2=0;
Int_t zerod3=0;
Int_t zerod4=0;
Int_t zerod5=0;

myCompt=0;

while (1) 
   {
      ncols = fscanf(fp,"%f %f %f %f %f %f %f",&e,&trans,&d1,&d2,&d3,&d4,&d5);
      if (ncols < 0) break;
      
      if (e==tab_e[comptter])
      {
        tmpd1=0;tmpd2=0;tmpd3=0;tmpd4=0;tmpd5=0;
	
         if ((e+10.79)/2. > e) max1=e;
         else max1 = (e+10.79)/2.;
	 
         if ((e+13.39)/2. > e) max2=e;
         else max2 = (e+13.39)/2.;
	 
         if ((e+16.05)/2. > e) max3=e;
         else max3 = (e+16.05)/2.;
	 
         if ((e+32.30)/2. > e) max4=e;
         else max4 = (e+32.30)/2.;
	 
         if ((e+539.)/2. > e) max5=e;
         else max5 = (e+539.)/2.;	 
	 
        if (trans>=10.79&&trans<=max1) sumd1=sumd1+(all_xs1[myCompt]+all_xs1[myCompt-1])*0.5*width_e[myCompt];
        if (trans>=13.39&&trans<=max2) sumd2=sumd2+(all_xs2[myCompt]+all_xs2[myCompt-1])*0.5*width_e[myCompt];
        if (trans>=16.05&&trans<=max3) sumd3=sumd3+(all_xs3[myCompt]+all_xs3[myCompt-1])*0.5*width_e[myCompt];
        if (trans>=32.30&&trans<=max4) sumd4=sumd4+(all_xs4[myCompt]+all_xs4[myCompt-1])*0.5*width_e[myCompt];
        if (trans>=539.0&&trans<=max5) sumd5=sumd5+(all_xs5[myCompt]+all_xs5[myCompt-1])*0.5*width_e[myCompt];
	
	if (d1cum[comptter]!=0&&zerod1==0) tmpd1= sumd1/d1cum[comptter];
	if (d2cum[comptter]!=0&&zerod2==0) tmpd2= sumd2/d2cum[comptter];
	if (d3cum[comptter]!=0&&zerod3==0) tmpd3= sumd3/d3cum[comptter];
	if (d4cum[comptter]!=0&&zerod4==0) tmpd4= sumd4/d4cum[comptter];
	if (d5cum[comptter]!=0&&zerod5==0) tmpd5= sumd5/d5cum[comptter];
	
	if (d1cum[comptter]!=0&&zerod1==1) tmpd1= 2;
	if (d2cum[comptter]!=0&&zerod2==1) tmpd2= 2;
	if (d3cum[comptter]!=0&&zerod3==1) tmpd3= 2;
	if (d4cum[comptter]!=0&&zerod4==1) tmpd4= 2;
	if (d5cum[comptter]!=0&&zerod5==1) tmpd5= 2;
	
	fprintf (fpout,"%15.9e %15.9e %15.9e %15.9e %15.9e %15.9e %15.9e \n",double(e),double(trans),double(tmpd1),double(tmpd2),double(tmpd3),double(tmpd4),double(tmpd5));
		
	//cout << tab_e[comptter] << " " << sumd1 << endl;
	
	//cout << e << " " << trans << " " << tmpd1 << endl;
	
	if (tmpd1==1) {zerod1=1;}
	if (tmpd2==1) {zerod2=1;}
	if (tmpd3==1) {zerod3=1;}
	if (tmpd4==1) {zerod4=1;}
	if (tmpd5==1) {zerod5=1;}
	
      }

      if (e!=tab_e[comptter])
      {
        zerod1=0;zerod2=0;zerod3=0;zerod4=0;zerod5=0;
	comptter++;
        tmpd1=0;tmpd2=0;tmpd3=0;tmpd4=0;tmpd5=0;
        sumd1=0;sumd2=0;sumd3=0;sumd4=0;sumd5=0;
	
         if ((e+10.79)/2. > e) max1=e;
         else max1 = (e+10.79)/2.;
	 
         if ((e+13.39)/2. > e) max2=e;
         else max2 = (e+13.39)/2.;
	 
         if ((e+16.05)/2. > e) max3=e;
         else max3 = (e+16.05)/2.;
	 
         if ((e+32.30)/2. > e) max4=e;
         else max4 = (e+32.30)/2.;
	 
         if ((e+539.)/2. > e) max5=e;
         else max5 = (e+539.)/2.;	 
	 
         if (trans>=10.79&&trans<=max1)  sumd1=(all_xs1[myCompt]+all_xs1[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=13.39&&trans<=max2)  sumd2=(all_xs2[myCompt]+all_xs2[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=16.05&&trans<=max3)  sumd3=(all_xs3[myCompt]+all_xs3[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=32.30&&trans<=max4)  sumd4=(all_xs4[myCompt]+all_xs4[myCompt-1])*0.5*width_e[myCompt];
         if (trans>=539.0&&trans<=max5)  sumd5=(all_xs5[myCompt]+all_xs5[myCompt-1])*0.5*width_e[myCompt];
	
	if (d1cum[comptter]!=0) tmpd1= sumd1/d1cum[comptter];
	if (d2cum[comptter]!=0) tmpd2= sumd2/d2cum[comptter];
	if (d3cum[comptter]!=0) tmpd3= sumd3/d3cum[comptter];
	if (d4cum[comptter]!=0) tmpd4= sumd4/d4cum[comptter];
	if (d5cum[comptter]!=0) tmpd5= sumd5/d5cum[comptter];
	
//	fprintf (fpout,"%f %f %f %f %f %f %f \n",e,trans,tmpd1,tmpd2,tmpd3,tmpd4,tmpd5);
	fprintf (fpout,"%15.9e %15.9e %15.9e %15.9e %15.9e %15.9e %15.9e \n",double(e),double(trans),double(tmpd1),double(tmpd2),double(tmpd3),double(tmpd4),double(tmpd5));
      
      }
      
      myCompt++;
      
   }
fclose(fpout);
fclose(fp);

  
}
