from sunpy.map import Map 
from sunpy.instr.aia import aiaprep as AP
from skimage.transform import resize as R
import numpy as np
import os
from pandas import read_csv

class sdo_prep:
    def __init__(self, csv_degradation='./aia_degradation_v8.csv'):
        if os.path.exists(csv_degradation):
            self.db_degradation = read_csv(csv_degradation)

    def t_rec_to_date(self, t_rec):
        year = t_rec[0:4]
        month = t_rec[5:7]
        day = t_rec[8:10]
        hour = t_rec[11:13]
        date = '%s-%s-%s-%s-00-00'%(year, month, day, hour)
        return date

    def from_sunpy(self, file_):
        M = AP(Map(file_))
        meta = M.meta
        data = M.data
        return meta, data

    def degradation(self, meta, data):
        wavelnth = meta['WAVELNTH']
        if wavelnth in (94, 131, 171 ,193, 211, 304, 335):
            t_rec = meta['T_REC']
            date = self.t_rec_to_date(t_rec)
            w = np.where(self.db_degradation['date'] == date)
            dg_factor = self.db_degradation[str(wavelnth)][w[0][0]]
        elif wavelnth in (1600, 1700, 4500):
            dg_factor = 1.
        data = data * dg_factor
        return data

    def norm_exposure(self, meta, data):
        exptime = meta['EXPTIME']
        data = data/exptime
        meta['PIXLUNIT'] = 'DN/sec'
        meta['LVL_NUM'] = 1.8
        meta['EXPTIME'] = 1.0
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
        meta['NAXIS1'] = self.isize_target
        meta['NAXIS2'] = self.isize_target
        meta['LVL_NUM'] = 2.0
        meta['CDELT1'] = meta['cdelt1']/ratio
        meta['CRPIX1'] = self.isize_target//2 + 0.5
        meta['CDELT2'] = meta['cdelt2']/ratio
        meta['CRPIX2'] = self.isize_target//2 + 0.5
        meta['R_SUN'] = self.rsun_target
        return meta, data_new

    def __call__(self, file_):
        meta1, data1 = self.from_sunpy(file_)
        meta1, data1 = self.norm_exposure(meta1, data1)
        data1 = self.degradation(meta1, data1)
        meta2, data2 = self.resize(meta1, data1)
        result = {'lev1.8':{'meta':meta1, 'data':data1}, 'lev2.0':{'meta':meta2, 'data':data2}}
        return result


if __name__ == '__main__' :
    from glob import glob
    from imageio import imsave
    list_ = glob('*.fits')
    nb = len(list_)
    print(nb)
    P = sdo_prep_and_resize_by_pixel(1024, 392)
    for file_ in list_ :
        result = P(file_)
        lev1 = result['lev1.8']
        lev2 = result['lev2.0']
        lev1_meta = lev1['meta']
        lev1_data = lev1['data']
        lev2_meta = lev2['meta']
        lev2_data = lev2['data']
        print(lev1_meta['R_SUN'], lev1_meta['CDELT1'], lev1_meta['CRPIX1'], lev1_meta['EXPTIME'], lev1_data.shape)
        print(lev2_meta['R_SUN'], lev2_meta['CDELT1'], lev2_meta['CRPIX1'], lev2_meta['EXPTIME'], lev2_data.shape)
#        np.save('%s.npy'%(file_), data)
#        imsave('%s.png'%(file_), (np.log10((data+1.).clip(1, 10.**4.))*(255./4.)).astype(np.uint8))






