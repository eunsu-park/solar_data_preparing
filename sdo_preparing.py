from sunpy.map import Map 
from sunpy.instr.aia import aiaprep as AP
from skimage.transform import resize as R
import numpy as np


class sdo_prep:
    def __init__(self):
        return 0

    def from_sunpy(self, file_):
        M = AP(Map(file_))
        meta = M.meta
        data = M.data
        return meta, data

    def degradation(self, meta, data):

        dg_factor = 1.
        data = data * dg_factor
        return data

    def norm_exposure(self, meta, data):
        exptime = meta['EXPTIME']
        data = data/exptime
        meta['PIXLUNIT'] = 'DN/sec'
        meta['LVL_NUM'] = 1.8
        return meta, data

    def __call__(self, file_):
        meta, data = self.from_sunpy(file_)
        meta, data = self.norm_exposure(meta, data)
        data = self.degradation(meta, data)
        return meta, data


class sdo_prep_and_resize_by_pixel(sdo_prep):
    def __init__(self, isize_target, rsun_target):
        super(sdo_prep_and_resize_by_pixel, self).__init__()
        if type(isize_target) != int :
            raise TypeError('Type(isize_target) == integer')
        elif isize_target % 2 != 0 :
            raise ValueError('isize_target%2 == 0')
        else :
            self.isize_target = isize_target

        if type(rsun_target) != int :
            raise TypeError('Type(rsun_target) == integer')
        elif rsun_target % 2 != 0 :
            raise ValueError('rsun_target%2 == 0')
        else:
            self.rsun_target = rsun_target

    def resize(self, meta, data):
        isize_orig = meta['NAXIS1']
        rsun_orig = meta['R_SUN']
        ratio = self.rsun_target/rsun_orig
        isize_new = int(isize_orig*ratio)
        pcsize = (self.isize_target - isize_new)//2
        if isize_new % 2 != 0 :
            isize_new += 1
        data_new = R(data, (isize_new, isize_new), order = 1, mode='constant', preserve_range=True)
        if pcsize > 0 :
            data_new = np.pad(data_new, pcsize, mode='constant', constant_values=0)
        elif pcsize < 0:
            data_new = data_new[pcsize:-pcsize, pcsize:-pcsize]
        else :
            pass
        meta['naxis1'] = self.isize_target
        meta['naxis2'] = self.isize_target
        meta['LVL_NUM'] = 2.0
        meta['cdelt1'] = meta['cdelt1']/ratio
        meta['crpix1'] = self.isize_target//2 + 0.5
        meta['cdelt2'] = meta['cdelt2']/ratio
        meta['crpix2'] = self.isize_target//2 + 0.5
        meta['r_sun'] = self.rsun_target
        return meta, data_new

    def __call__(self, file_):
        meta, data = self.from_sunpy(file_)
        meta, data = self.norm_exposure(meta, data)
        data = self.degradation(meta, data)
        meta, data = self.resize(meta, data)
        return meta, data


if __name__ == '__main__' :
    from glob import glob
    from imageio import imsave
    list_ = glob('*.fits')
    nb = len(list_)
    print(nb)
    P = sdo_prep_and_resize_by_pixel(1024, 392)
    for file_ in list_ :
        meta, data = P(file_)
        print(meta['r_sun'], meta['cdelt1'], meta['crpix1'], data.shape)
        imsave('%s.png'%(file_), (np.log10((data+1.).clip(1, 10.**4.))*(255./4.)).astype(np.uint8))





