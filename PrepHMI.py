import numpy as np
from sunpy.map import Map
from sunpy.instr.aia import aiaprep
#import astropy.units as u
#from sunpy.image.rescale import resample
from sunpy.io import fits
import os, glob
from imageio import imsave

def main(M):

    M_new = aiaprep(M)
    t_rec = M_new.meta['t_rec']
    type_instr = M_new.meta['content'][0] + '_' + str(int(M_new.meta['cadence'])) + 'S'

    datetime = t_rec[0:4] + '_' + t_rec[5:7] + '_' + t_rec[8:10] + '_' + t_rec[11:13] + '_' + t_rec[14:16] + '_' + t_rec[17:19]
    year, month, day, hour, minute, second = np.array([t_rec[0:4], t_rec[5:7], t_rec[8:10], t_rec[11:13], t_rec[14:16], t_rec[17:19]], dtype = np.int)
    date = (year, month, day, hour, minute, second)

    return type_instr, datetime, date, M_new


root_load = '/home/joshua/NAS/HMI/M_720S/'
root_save = '/home/joshua/github_storage/datasets/HMI/M_720S/'

year = int(input('Year?     '))

month = 1
while month <= 12 :

    day = 1
    while day <= 31 :

        hour = 0
        while hour <= 23 :

            name_fits = 'HMI_M_720S_%04d_%02d_%02d_%02d_00_00.fits' % (year, month, day, hour)
            name_png = 'HMI_M_720S_%04d_%02d_%02d_%02d_00_00.png' % (year, month, day, hour)

            path_load = root_load + '%04d/%02d/%02d/' % (year, month, day)
            path_save = root_save + '%04d/%02d/%02d/' % (year, month, day)

            name_load = path_load + name_fits
            name_save = path_save + name_fits

            list_load = sorted(glob.glob(name_load))
            list_save = sorted(glob.glob(name_save))

#            print(name_fits, len(list_load), len(list_save))

            if len(list_load) > 0  and len(list_save) == 0:

                file_fits = list_load[0]
                M = Map(file_fits)
                type_instr, datetime, date, M_new = main(M)
                os.makedirs(path_save, mode = 0o777, exist_ok = True)
                fits.write(name_save, np.array(M_new.data, dtype=np.float32), M_new.meta)
                imsave(path_save + name_png, M_new.data.clip(-100, 100))

                print(name_save)


#                quality = M.meta['quality']
#                print(file_fits, quality)

#            file_fits = root_load + '%04d/%02d/%02d/HMI_M_720S_%04d_%02d_%02d_%02d_00_00.fits' % (year, month, day, year, month, day, hour)
#            path_save = root_save + '%04d/%02d/%02d/' % (year, month, day)
#            name_save = path_save + 'HMI_M_720S_%04d_%02d_%02d_%02d_00_00.fits' % (year, month, day, hour)
#            fits_check = glob.glob(name_save)

            

#            M = Map(file_fits)                
#            assert M.meta['detector'].lower() == 'hmi', 'This fits file is not HMI'
#            quality = M.meta['quality']

#            if int(quality) == 0 and len(fits_check) == 0 :

#                type_instr, datetime, date, M_new = main(M)
#                os.makedirs(path_save, mode = 0o777, exist_ok = True)
#                fits.write(name_save, np.array(M_new.data, dtype=np.float32), M_new.meta)
#                print(name_save)

            hour += 6
        day += 1
    month += 1

#conda activate sunpy ; python PrepHMI.py

