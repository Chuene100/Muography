
Mihaly Novak 
May 2020
CERN

This directory contains data used by the 'G4eDPWAElasticDCS' class. 

The 'dcss' sub-directory
------------------------

Contains numerical Differential Cross Sections (DCS) for e-/e+ Coulomb 
scattering computed by Dirac Partial Wave Analysis (DPWA) using ELSEPA [1]: 
- electrostatic interaction, with a local exchange correction in the case of 
  electrons (using Dirac-Fock e- densities; finite nuclear size with Fermi 
  charge distribution; exchange potential with Furness and McCarthy for e-) [2]
- correlation-polarization (projectiles cause the polarization of the charge 
  cloud of the target atom and the induced dipole moment acts back on the 
  projectile) was accounted by using Local-Density Approximation (LDA) [2]
- absorption: not included since it's an inelastic channel [2](the corresponding  
  excitations needs to be modelled by a separate, independent, inelastic model).
  
The DCS have been computed at 106 e-/e+ kinetic energy points from 10 [eV] to 
100 [MeV] over two different theta (polar angle of scattering) grids: one dense 
grid with 247 theta values used only in case of e- below 2 [keV] kinetic 
energies and an other one with 128 theta values used for e+ (all energies) and 
e- above 2 [keV] kinetic energies. The dense grid was introduced to describe 
appropriately the deep minimum (Ramsauer–Townsend effect) of the DCS (only e-) 
and it corresponds to energy index range of [0-35) while the sparse grid is 
sufficient for energy index range [35-106) (E>2 [keV]). The lower part [0-35) 
is stored in files ending with '_l' while the higher part [35-106) with '_h'.
Note, that for e+ the theta grid with 128 points is sufficient for all energies.
Also note, that using the above mentioned DPWA computation with a free atom 
approximation might lead to questionable results below few hundred [eV] where 
possible solid state or bounding effects might start to affect the potential.
Nevertheless, the lower energy was set to 10 eV in order to provide (at least)
some model even at low energies (with this caution).


The 'stables' sub-directory
--------------------------- 

The numerical DCS are utilised to provide samples of scattering angles as a 
function of the target atomic number Z, projectile type (e- or e+) and kinetic 
energy E (between 10 [eV] and 100 [MeV]). A variable transformation is used in 
order to make producing samples according to these numerical distributions 
possible while storing manageable size of data. The polar scattering angle 'th'
is transformed to 'mu(th)=0.5[1-cos(th)]' which is further transformed to 
'u(mu)=(A+1)mu/(A+mu)' with the screening parameter 'A=0.5 sig1/sig' with 
the elastic (sig) and first transport cross section (sig1). This would transform
the screened Rutherford DCS based pdf to a uniform, i.e. very smooth, 
distribution (with the proper value of A) [3].  

An appropriate u-grid (or actually 2) can be generated based on the provided 
theta grids as 'mu(th) = 0.5[1-cos(th)]' and 'u(mu; A'=0.01)=(A'+1)*mu/(A'+mu)'. 
Then the transformed 'p(u)=p(mu)/[A(A+1)/(A+mu)^2]' pdf with the original 
'p(mu)=4pi[ds/dOmega]/sig' can be computed. This transformation from 'th'->'mu'
and actually from 'mu'->'u' makes the corresponding pdf significantly smoother,
better for numerical sampling and reducing the size of the required data points.

Producing samples 'u' from the numerical 'p(u)' can be done in two ways:
 - using Alias table based (discrete) sampling of an 'u' value bin + numerical 
   inversion of the cumulative, sampled within the corresponding cumulative 
   interval (continuous): very fast but the Alias part destroys the monotonic 
   property i.e. sampling from a restricted (dynamic) 'u' value interval is not 
   possible
 - as above without the Alias part i.e. numerical inversion of the cumulative:
   requires binary search to locate the cumulative interval where the given 
   sample lies to (since Alias is not available) which makes it a bit slower.
The first version can be utilised when the DPWA DCS are used to build up a pure 
single scattering model when each individual interactions are modelled (i.e.
sampling form the entire 'th [0,pi]' range are required). While the second can 
provide a solution in case of mixed simulation models when "hard collisions"
(elastic scattering resulting angular deflection higher than a given dynamic i.e. 
energy dependent threshold) requires samples of polar scattering angle above a 
given (dynamic) limit.

The union of these, i.e. the combination of the Alias method for discrete 
with a rational interpolation based numerical inversion of the cumulative for 
the continuous part, has been used to produce the necessary data for each DCS 
i.e. each particle (e-/e+), for each target Z (1-103) and kinetic energy points 
(106 from 10 [eV] 100 [MeV]). These data, stored under the 'stables' 
sub-directory, makes possible the accurate and fast sampling of the angular 
deflection according to these numerical DCS.  


References
----------

[1] Salvat, F., Jablonski, A. and Powell, C.J., 2005. ELSEPA—Dirac partial-wave 
    calculation of elastic scattering of electrons and positrons by atoms, 
    positive ions and molecules. Computer physics communications, 165(2),
    pp.157-190.
[2] Salvat, F., 2003. Optical-model potential for electron and positron elastic 
    scattering by atoms. Physical Review A, 68(1), p.012708.
[3] Benedito, E., Fernández-Varea, J.M. and Salvat, F., 2001. Mixed simulation 
    of the multiple elastic scattering of electrons and positrons using 
    partial-wave differential cross-sections. Nuclear Instruments and Methods 
    in Physics Research Section B: Beam Interactions with Materials and Atoms, 
    174(1-2), pp.91-110.   
   


