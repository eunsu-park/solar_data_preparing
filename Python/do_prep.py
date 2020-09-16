import warnings
warnings.filterwarnings('ignore')

import sunpy
import aiapy.psf
from astropy import units as u
from aiapy.calibrate import register, update_pointing
from aiapy.calibrate import correct_degradation
from aiapy.calibrate.util import get_correction_table

def run_deconv(m, iterations=25):
    psf = aiapy.psf.psf(m.wavelength)
    m_deconvolved = aiapy.psf.deconvolve(m, psf=psf, iterations=iterations)
    return m_deconvolved

def run_prep(m):
    m_updated_pointing = update_pointing(m)
    m_registered = register(m_updated_pointing)
    data_normalized = m_registered.data/m_registered.exposure_time.to(u.s).value
    meta_normalized = m_registered.meta
    meta_normalized['EXPTIME'] = 1.0
    m_normalized = sunpy.map.Map(data_normalized, meta_normalized)
    return m_normalized

class aia_prep:
    def __init__(self, do_deconv=False, do_degrad=True):
        self.do_deconv = do_deconv
        self.do_degrad = do_degrad
        if self.do_degrad :
            self.correction_table = get_correction_table()
    def __call__(self, file_):
        m = sunpy.map.Map(file_)
        if self.do_deconv :
            m = run_deconv(m)
        m = run_prep(m)
        if self.do_degrad :
            m = correct_degradation(m, correction_table=self.correction_table)
        return m

if __name__ = '__main__' :

    do_deconv=False # Deconvolution
    do_degrad=True # Degradation
    
    aiaprep = aia_prep(do_deconv=do_deconv, do_degrad=do_degrad)

    file_fits = 'path/to/fits'
    M_preped = aiaprep(file_fits)
    print(M_preped)