{

gROOT->Reset();

char informat[] = "../pairdata/pp-pair-cs-%d.dat";
char outformat[] = "pp-pair-cs-%d.dat";
char infn[20];
char outfn[20];
Float_t nrj,sig,emin,emax;
Int_t ncols,nlines,nlinesbis;

for (int numero = 1; numero < 100; numero++)
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
      nlines = nlines+1;
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
      fprintf (fpout,"%e %e\n",nrj,sig*1e-22); // to convert barns into mm*mm
      nlinesbis=nlinesbis+1;
   }

fclose(fpin);
fclose(fpout);

}

}

