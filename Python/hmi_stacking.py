from sunpy.map import Map
import numpy as np
from scipy.ndimage import interpolation
from aiapy.calibrate import register
import warnings
warnings.filterwarnings('ignore')

class stacking:
    def __init__(self, nb_stack=21, solar_rot_period=25.38):
        self.nb_stack = nb_stack
        self.solar_rot_period = solar_rot_period

    def run_subpix(self, list_fits):
        M = Map(sorted(list_fits))
        M = [register(M[n]) for n in range(self.nb_stack)]
        results = []
        for idx in range(self.nb_stack):
            m = M[idx]
            meta = m.meta
            data = m.data[2048-256:2048+256, 2048-256:2048+256]
            rsun = meta['R_SUN']
            shift_idx = idx - float(self.nb_stack//2)
            angle = (shift_idx*360.*np.pi) / (self.solar_rot_period*24.*80.*180.)
            shift = rsun * np.sin(angle) * -1.
            data_shift = interpolation.shift(data, (0.0, shift), order=3)
            results.append(data_shift)
        return results
        
    def __call__(self, list_fits):
        results = self.run_subpix(list_fits)
        return results





if __name__ == '__main__' :
    from glob import glob
    import matplotlib.pyplot as plt
    from imageio import imsave

    root = '/userhome/park_e/Datasets/hmi_denoising'
    year = 2011
    month = 1
    day = 1
    hour = 0

    list_ = glob('%s/%04d/%02d/%02d/%02d/*.fits'%(root, year, month, day, hour))
    nb = len(list_)
    print(nb)

    hs = stacking()
    results = hs(list_)
    print(len(results))
    for n in range(len(results)):
        tmp = results[n].clip(-30, 30)
        imsave('%02d.png'%(n), tmp)
        

    

