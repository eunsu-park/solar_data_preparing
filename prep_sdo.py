import numpy as np
from sunpy.map import Map
from sunpy.instr.aia import aiaprep
import astropy.units as u
from sunpy.image.rescale import resample


def bytescale(data, bmin, bmax):
    bdiff = bmax - bmin
    data = data.clip(bmin, bmax)
    data = ((data - bmin)/bdiff * 255.).astype('uint8')
    return data

def aia_bytescale(data, wavelnth):
    if not wavelnth in [94, 131, 171, 193, 211, 304, 335, 1600, 1700, 4500] :
        raise NameError('Incorrect Wavelength!')
    scales = {  '94' : (4.99803,  1.5,    50.),  '131' : (6.99685,  7.0,  1200.),
               '171' : (4.99803,  10.,  6000.),  '193' : (2.99950, 120.,  6000.),
               '211' : (4.99801,  30., 13000.),  '304' : (4.99941,  50.,  2000.),
               '335' : (6.99734,  3.5,  1000.), '1600' : (2.99911,   0.,  1000.),
              '1700' : (1.00026,   0.,  2500.), '4500' : (1.00026,   0., 26000.)}
    logs = [131, 193, 211, 304, 335]
    sqrts = [94, 171]
    bfactor, bmin, bmax = scales[str(wavelnth)]
    data = data * bfactor
    if wavelnth in logs :
        data_bytscl = bytescale(np.log10(data), np.log10(bmin), np.log10(bmax))
    elif wavelnth in sqrts :
        data_bytscl = bytescale(np.sqrt(data), np.sqrt(bmin), np.sqrt(bmax))
    else :
        data_bytscl = bytescale(data, bmin, bmax)
    return data_bytscl

def circle_cutting(data, isize, rsun, cmin):
    for i in range(isize):
        for j in range(isize):
            if (i-isize/2.)**2. + (j-isize/2.)**2. > (rsun-1.) ** 2. :
                data[i, j] = cmin
    return data

def find_ratio(wavelnth, year, month, day, hour):
    if wavelnth in [94, 131, 171, 193, 211, 304, 335] :
        time_format = '%04d-%02d-%02dT%02d:00:00' % (year, month, day, hour)
        read = open('./ratios/ratio_aia_%d_%04d.txt' % (wavelnth, year), 'r')
        for line in read.readlines():
            date = line[0:19]
            if date == time_format :
                ratio = float(line[19:])
                break
    else :
        ratio = 1.
    return ratio

def prep_and_resize(fits, isize_target, rsun_target):

    map_sdo = Map(fits)

    detector = map_sdo.meta['detector']
    wavelnth = map_sdo.meta['wavelnth']
    quality = map_sdo.meta['quality']
    t_rec = map_sdo.meta['t_rec']
    
    if not detector.lower() in ['aia', 'hmi'] : raise NameError('This fits file is neither AIA nor HMI')

    if detector.lower() == 'aia' :
        type_instr = str(wavelnth)
    else :
        type_instr = map_sdo.meta['content'][0] + '_' + str(int(map_sdo.meta['cadence'])) + 'S'

    date = t_rec[0:4] + '_' + t_rec[5:7] + '_' + t_rec[8:10] + '_' + t_rec[11:13] + '_' + t_rec[14:16] + '_' + t_rec[17:19]
    year, month, day, hour, minute, second = np.array([t_rec[0:4], t_rec[5:7], t_rec[8:10], t_rec[11:13], t_rec[14:16], t_rec[17:19]], dtype = np.int)

    if quality == 0 :

        map_prep = aiaprep(map_sdo)
        meta = map_prep.meta
        rsun = meta['r_sun']
        isize = meta['naxis1']

        if detector == 'aia' :    
            ratio = find_ratio(wavelnth, year, month, day, hour)
            data = map_prep.data * ratio / meta['exptime']
        else :
            data = np.where(np.isnan(map_prep.data), -5000, map_prep.data)

        isize_mid = int(isize * rsun_target / rsun)
        if isize_mid % 2 != 0 :
            isize_mid += 1 

        pcsize = (isize_target - isize_mid)//2
        data_mid = resample(data, (isize_mid, isize_mid)*u.pixel, method = 'linear', center = True)

        if pcsize > 0 :
            data_new = np.pad(data_mid, pcsize, mode = 'constant')
        elif pcsize < 0 :    
            data_new = data_mid[pcsize:-pcsize, pcsize:-pcsize]
        else :
            data_new = data_mid

        if detector.lower() == 'hmi' :
            data_final = circle_cutting(data_new, isize_target, rsun_target, -5000.)
        else :
            data_final = data_new

    else :
        data_final = None

    summary = {'date':date, 'detector':detector, 'type':type_instr, 'quality':quality}
    
    return data_final, summary
