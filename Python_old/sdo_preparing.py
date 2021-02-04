from sunpy.map import Map 
from sunpy.instr.aia import aiaprep as AP
from skimage.transform import resize as R
import numpy as np
import os
from pandas import read_csv


class sdo_prep:
    def __init__(self, resize=False, isize=None, rsun=None):
        if resize == True:
            if isize :
                if type(isize) != int :
                    raise TypeError('Type(isize) == integer')
                elif isize % 2 != 0 :
                    raise ValueError('isize%2 == 0')
                else :
                    self.isize = isize
            else :
                raise NotImplementedError('resize:True but isize is not implemented')
            if rsun :
                if type(rsun) != int :
                    raise TypeError('Type(rsun) == integer')
                else:
                    self.rsun = rsun
            else :
                raise NotImplementedError('resize:True but rsun is not implemented')
        self.resize = resize

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

    def resize_by_pixel(self, meta, data, pvalue=0):
        isize_orig = meta['NAXIS1']
        rsun_orig = meta['R_SUN']
        ratio = self.rsun/rsun_orig
        isize_new = int(isize_orig*ratio)
        if isize_new % 2 != 0 :
            isize_new += 1
        pcsize = (self.isize - isize_new)//2
        data_new = R(data, (isize_new, isize_new), order = 1, mode='constant', preserve_range=True)
        if pcsize > 0 :
            data_new = np.pad(data_new, pcsize, mode='constant', constant_values=pvalue)
        elif pcsize < 0:
            data_new = data_new[pcsize:-pcsize, pcsize:-pcsize]
        else :
            pass
        meta['NAXIS1'] = self.isize
        meta['NAXIS2'] = self.isize
        meta['LVL_NUM'] = 2.0
        meta['CDELT1'] = meta['cdelt1']/ratio
        meta['CRPIX1'] = self.isize//2 + 0.5
        meta['CDELT2'] = meta['cdelt2']/ratio
        meta['CRPIX2'] = self.isize//2 + 0.5
        meta['R_SUN'] = self.rsun
        return meta, data_new


class hmi_prep(sdo_prep):
    def __init__(self, resize=False, isize=None, rsun=None):
        super(hmi_prep, self).__init__(resize, isize, rsun)
        X = np.arange(4096)[:, None]
        Y = np.arange(4096)[None, :]
        self.XY = np.sqrt((X-2048.)**2. + (Y-2048.)**2.)

    def cut_radius(self, meta, data):
        r_sun = meta['R_SUN']
        Z = np.where(self.XY > r_sun)
        data[Z] = -5000.
        meta['LVL_NUM'] = 1.5
        return meta, data

    def __call__(self, file_):
        meta1, data1 = self.from_sunpy(file_)
        meta1, data1 = self.cut_radius(meta1, data1)
        result = {'lev1.5':{'meta':meta1, 'data':data1}, 'lev2.0':None}
        if self.resize == True :
            meta2, data2 = self.resize_by_pixel(meta1.copy(), data1.copy(), pvalue=-5000)
            result['lev2.0'] = {'meta':meta2, 'data':data2}
        return result

class aia_prep(sdo_prep):
    def __init__(self, csv_degradation='./aia_degradation_v8.csv', resize=False, isize=None, rsun=None):
        super(aia_prep, self).__init__(resize, isize, rsun)
        if os.path.exists(csv_degradation):
            self.db_degradation = read_csv(csv_degradation)

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
        return meta, data

    def norm_exposure(self, meta, data):
        exptime = meta['EXPTIME']
        data = data/exptime
        meta['PIXLUNIT'] = 'DN/sec'
        meta['LVL_NUM'] = 1.5
        meta['EXPTIME'] = 1.0
        return meta, data

    def __call__(self, file_):
        meta1, data1 = self.from_sunpy(file_)
        meta1, data1 = self.norm_exposure(meta1, data1)
        meta1, data1 = self.degradation(meta1, data1)
        result = {'lev1.5':{'meta':meta1, 'data':data1}, 'lev2.0':None}
        if self.resize == True :
            meta2, data2 = self.resize(meta1.copy(), data1.copy())
            result['lev2.0'] = {'meta':meta2, 'data':data2}
        return result
