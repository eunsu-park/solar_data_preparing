import warnings
warnings.filterwarnings('ignore')
from sunpy.map import Map
from aiapy.calibrate import register, update_pointing
import aiapy.psf
from aiapy.calibrate import correct_degradation
from aiapy.calibrate.util import get_correction_table


def run_deconv(m, iterations=25):
    psf = aiapy.psf.psf(m.wavelength)
    m_deconvolved = aiapy.psf.deconvolve(m, psf=psf, iterations=iterations)
    return m_deconvolved


class SDOPrep:
    def __init__(self, do_update_pointing=False):
        self.do_update_pointing=do_update_pointing

    def read(self, list_fits):
        list_M = Map(list_fits)
        return list_M

    def update_pointing(self, list_M):
        if type(list_M) == list :
            list_M = [update_pointing(list_M[n]) for n in range(len(list_M))]
        elif type(list_M) == str :
            list_M = update_pointing(list_M)
        return list_M

    def register(self, list_M):
        if type(list_M) == list :
            list_M = [register(list_M[n]) for n in range(len(list_M))]
        elif type(list_M) == str :
            list_M = register(list_M)
        return list_M

    def __call__(self, list_fits):
        list_M = self.read(list_fits)
        if self.do_update_pointing == True :
            list_M = self.update_pointing(list_M)
        list_M = self.register(list_M)
        return list_M


class HMIPrep(SDOPrep)
    def __init__(self, do_update_pointing=False):
        super(HMIPrep, self).__init__(self, do_update_pointing=do_update_pointing)
    def __call__(self, list_fits):
        list_M = self.read(list_fits)
        if self.do_update_pointing == True :
            list_M = self.update_pointing(list_M)
        list_M = self.register(list_M)
        return list_M

class AIAPrep(SDOPrep)
    def __init__(self, do_update_pointing=False, correct_degradation=True):
        super(AIAPrep, self).__init__(self, do_update_pointing=do_update_pointing)
        self.correct_degradation = correct_degradation
        if self.do_correct_degradation :
            self.correction_table = get_correction_table()

    def degradation(self, list_M):
        if type(list_M) == list :
            list_M = [correct_degradation(list_M[n], correction_table=self.correction_table) for n in range(len(list_M))]
        elif type(list_M) == str :
            list_M = correct_degradation(list_M, correction_table=self.correction_table)
        return list_M

    def __call__(self list_fits):
        list_M = self.read(list_fits)
        if self.do_update_pointing == True :
            list_M = self.update_pointing(list_M)
        list_M = self.register(list_M)
        if self.correct_degradation == True :
            list_M = self.degradation(list_M)
        return list_M
