{

gROOT->Reset();

char informat[] = "re-cs-%d.dat";
char outformat[] = "../rayl-2012/re-cs-%d.dat";
char infn[20];
char outfn[20];
Float_t nrj,sig,emin,emax;
Int_t ncols,nlines,nlinesbis;

for (int numero = 1; numero < 101; numero++)
{

sprintf(infn,informat,numero);
sprintf(outfn,outformat,numero);

FILE * fpin = fopen(infn,"r");
FILE * fpout = fopen(outfn,"a");

nlines = 0;
emin=0;
emax=0;

while (1) 
   {
      ncols = fscanf(fpin,"%e %e",&nrj,&sig);
      if (ncols < 0) break;
      if (nrj < 0) break;
      // Only less than 10 MeV
      if (nrj<=10.) nlines = nlines+1; // We only care less than 1 MeV
      if (nrj>emax) emax=nrj;
      if (nlines==1) emin=nrj;
      cout << nlines << " " << nrj << " " << sig << endl;
   }

fclose(fpin);
cout << infn << endl;
cout << nlines << endl;
cout << emin << endl;
cout << emax << endl;

FILE * fpin = fopen(infn,"r");

nlinesbis=0;

while (1) 
   {
      ncols = fscanf(fpin,"%e %e",&nrj,&sig);
      if (ncols < 0) break;
      if (nrj < 0) break;
      if (nlinesbis==0) fprintf (fpout,"%e %e %i\n",emin, emax, nlines);
      if (nlinesbis==0) fprintf (fpout,"%i\n",nlines);
      // Only less than 10 MeV and times E*E
      if (nrj<10.) fprintf (fpout,"%e %e\n",nrj,nrj*nrj*sig*1e-22); // to convert barns into mm*mm
      nlinesbis=nlinesbis+1;
   }

fclose(fpin);
fclose(fpout);

}

}

