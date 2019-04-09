import numpy as np
from sunpy.map import Map
from sunpy.instr.aia import aiaprep
import astropy.units as u
from sunpy.image.rescale import resample
from numba import jit

def hmi_cutting(data_hmi, isize, rsun):
    data_hmi_new = np.where(np.isnan(data_hmi), np.nanmin(data_hmi), data_hmi)
    for i in range(isize):
        for j in range(isize):
            if (i-isize/2.)**2. + (j-isize/2.)**2. > (rsun-1.) ** 2. :
                data_hmi_new[i, j] = -5000
    return data_hmi_new

def find_ratio(wavelnth, year, month, day, hour):
    time_format = '%04d-%02d-%02dT%02d:00:00' % (year, month, day, hour)
    read = open('./ratios/ratio_aia_%d_%04d.txt' % (wavelnth, year), 'r')
    for line in read.readlines():
        date = line[0:19]
        if date == time_format :
            ratio = float(line[19:])
            break
    return ratio

@jit
def prep_and_resize(fits, isize_target, rsun_target):

    map_sdo = Map(fits)

    detector = map_sdo.meta['detector']
    wavelnth = map_sdo.meta['wavelnth']
    quality = map_sdo.meta['quality']
    t_rec = map_sdo.meta['t_rec']

    if detector == 'AIA':
        type_instr = str(wavelnth)
    elif detector == 'HMI' :
        type1 = map_sdo.meta['content'][0]
        type2 = str(int(map_sdo.meta['cadence'])) + 'S'
        type_instr = type1 + '_' + type2
    else :
        raise NameError('File is neither AIA nor HMI')

    date = t_rec[0:4] + '_' + t_rec[5:7] + '_' + t_rec[8:10] + '_' + t_rec[11:13] + '_' + t_rec[14:16] + '_' + t_rec[17:19]
    year, month, day, hour, minute, second = np.array([t_rec[0:4], t_rec[5:7], t_rec[8:10], t_rec[11:13], t_rec[14:16], t_rec[17:19]], dtype = np.int)

    if quality == 0 :

        map_prep = aiaprep(map_sdo)
        meta = map_prep.meta
        rsun = meta['r_sun']
        isize = meta['naxis1']

        if detector == 'AIA' :    
            if wavelnth in [94, 131, 171, 193, 211, 304, 335] :
                ratio = find_ratio(wavelnth, year, month, day, hour)
                data = map_prep.data * ratio / meta['exptime']
            else :
                data = map_prep.data / meta['exptime']
        elif detector == 'HMI' :
            data = np.where(np.isnan(map_prep.data), -5000, map_prep.data)
        else :
            raise NameError('File is neither AIA nor HMI')

        isize_mid = int(isize * rsun_target / rsun)
        isize_mid = int(isize * rsun_target / rsun)
        if isize_mid % 2 != 0 :
            isize_mid += 1 

        pocsize = (isize_target - isize_mid)//2
        data_mid = resample(data, (isize_mid, isize_mid)*u.pixel, method = 'linear', center = True)

        if pocsize > 0 :
            data_new = np.pad(data_mid, pocsize, mode = 'constant')
        elif picsize < 0 :    
            data_new = data_mid[pocsize:-pocsize, pocsize:-pocsize]
        else :
            data_new = data_mid

        if detector == 'AIA' :
            data_final = np.where(data_new <= 1., 0., np.log10(data_new))
        elif detector == 'HMI' :
            data_final = hmi_cutting(data_new, isize_target, rsun_target)/5000.

    else :
        data_final = None

    summary = {'date':date, 'detector':detector, 'type':type_instr, 'quality':quality}
    
    return data_final, summary






