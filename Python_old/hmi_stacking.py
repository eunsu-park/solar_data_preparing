from sunpy.map import Map
from sunpy.instr.aia import aiaprep
import numpy as np
from glob import glob
from utils_time import hmsm_to_days, date_to_jd, jd_to_date, days_to_hmsm
from sunpy.io import fits
from scipy.ndimage import interpolation

class stacking:

    def __init__(self, root_hmi, nb_stack=21, solar_rot_period=25.38):
        self.root_hmi = root_hmi
        if type(nb_stack) == int :
            self.nb_stack = nb_stack
        else :
            raise TypeError('Type(nb_stack): integer')
        if type(solar_rot_period) in [int, float] :
            self.solar_rot_period = float(solar_rot_period)
        else :
            raise TypeError('Type(solar_rot_period): integer or float')

    def make_list(self, year, month, day, hour):
        step = np.arange(self.nb_stack) - self.nb_stack//2
        list_tmp = []
        for n in range(self.nb_stack):
            jd = date_to_jd(year, month, day + hmsm_to_days(hour = hour, min = 0, sec = 0 + 0.001, micro = 0)) + step[n] * 45./86400.
            date = jd_to_date(jd)
            year_c, month_c, day_c = date[0], date[1], int(date[2])
            jd_decimal = date[2] - day_c
            hour_c, minute_c, second_c, _ = days_to_hmsm(jd_decimal)
            path_ = '%s/%04d/%02d/%02d' % (self.root_hmi, year_c, month_c, day_c)
            name_ = 'hmi.M_45s.%04d-%02d-%02d-%02d-%02d-%02d.fits' % (year_c, month_c, day_c, hour_c, minute_c, second_c)
            tmp = glob('%s/%s'%(path_, name_))
            if len(tmp) > 0 :
                list_tmp.append(tmp[0])
        return list_tmp

    def run_subpix(self, fits_hmi, index):
        map_hmi = aiaprep(Map(fits_hmi))
        data = map_hmi.data[2048-140:2048+140, 2048-140:2048+140]
        if index == self.nb_stack//2 :
            data_shift = data
        else :
            meta = map_hmi.meta
            shift_index = index - float(self.nb_stack//2)
            rsun = meta['r_sun']
            angle = (shift_index*360.*np.pi) / (self.solar_rot_period*24.*80.*180.)
            shift = rsun * np.sin(angle) * -1.
            data_shift = interpolation.shift(data, (0.0, shift), order=1)
        return data_shift

    def __call__(self, year, month, day, hour):
        list_ = self.make_list(year, month, day, hour)
        nb = len(list_)
        if nb == self.nb_stack :
            patches = []
            for n in range(self.nb_stack):
                patch = self.run_subpix(list_[n], n)
                patches.append(patch)
            center = patches[self.nb_stack//2]
            stacks = np.sum([patches[i] for i in range(self.nb_stack)], 0)/self.nb_stack
            center_256 = center[140-128:140+128, 140-128:140+128].astype(np.float32)
            stacks_256 = stacks[140-128:140+128, 140-128:140+128].astype(np.float32)
            print('%04d-%02d-%02d %02d UT: Successfully stacked (%d/%d)'%(year, month, day, hour, nb, self.nb_stack))
            return (center_256, stacks_256)
        else :
            center_256, stacks_256 = None, None
            print('%04d-%02d-%02d %02d UT: Not enough data number (%d/%d)'%(year, month, day, hour, nb, self.nb_stack))
            return None

if __name__ == '__main__' :

    root_hmi = ''
    
    SH = stacking(root_hmi, nb_stack=21)
    CS = SH(2011, 1, 1, 0)
    if CS :
        print(CS[0].shape, CS[1].shape)
        import matplotlib.pyplot as plt
        plt.imshow(np.hstack([CS[0], CS[1]]), vmin=-30, vmax=30)
        plt.show()



