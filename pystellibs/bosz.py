import numpy as np
from .simpletable import SimpleTable
try:
    from astropy.io import fits as pyfits
except ImportError:
    import pyfits

from .stellib import Stellib,AtmosphereLib
from .config import libsdir


class Bosz(Stellib):

    def __init__(self, R,v,*args, **kwargs):
        self.name = 'BOSZ_R{:.0f}_v{:.0f}'.format(R,v)
        self.source = libsdir+ "/"
        self._load_()
        Stellib.__init__(self, *args, **kwargs)

    def _load_(self):      
        self._getWaveLength_(self.source)
        self._getTGZ_(self.source)
        self._getSpectra_(self.source)
        self._getWaveLength_units(self.source)

    def _getWaveLength_(self, f):
        self._wavelength = np.load(f+self.name + "_wavelength.npy")

    def _getWaveLength_units(self, f):
        self.wavelength_unit = 'angstrom'

    def _getTGZ_(self, f):
        data = np.load(f+self.name + "_parameters.npy")
        dictionary = {}
        dictionary["Teff"] = data[:,0]
        dictionary["logg"] = data[:,1]
        dictionary["logT"] = data[:,2]
        dictionary["Z"] = data[:,3]
        dictionary["logZ"] = data[:,4]
        self.log_T_min = np.min(data[:,2])
        self.log_T_max = np.max(data[:,2])
        self.log_g_min = np.min(data[:,1])
        self.log_g_max = np.max(data[:,1])
        self.grid = SimpleTable(dictionary)


    def bbox(self, dlogT=0.05, dlogg=0.25):
        bbox = [
                (3.59,5.5),
                #(3.59,4.5),
                (4.07,5.0),
                (4.07,2.),
                #(3.82,2.),
                (3.845,1.),
                (3.74,0.),
                (3.62,-0.5),
                (3.4472,-0.5),
                (3.4472,5.5),
                (3.59,5.5),
                ]

        return np.array(bbox)

    def _getSpectra_(self, f):
        self.spectra = np.load(f+self.name + "_fluxes.npy").T


    @property
    def logg(self):
        return self.grid['logg']

    @property
    def logT(self):
        return self.grid['logT']

    @property
    def Teff(self):
        return self.grid['Teff']

    @property
    def Z(self):
        return self.grid['Z']

    @property
    def logZ(self):
        return self.grid['logZ']

    @property
    def NHI(self):
        return self.grid['NHI']

    @property
    def NHeI(self):
        return self.grid['NHeI']

    @property
    def NHeII(self):
        return self.grid['NHeII']
