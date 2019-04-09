

isize_target = 1024
rsun_target = 392

wavelnths = [94, 131, 171, 193, 211, 304, 335, 1600, 1700]

from prep_sdo import * #prep_and_resize
import glob, os
import numpy as np
from shutil import move

year = 2013
while year <= 2014 :

    month = 1
    while month <= 12 :

        day = 1
        while day <= 31 :

            hour = 0
            while hour <= 23 :

                list_sdo = []

                path_hmi = '/home/joshua/NAS/HMI/M_720S/%04d/%02d/%02d/' % (year, month, day)
                list_hmi = sorted(glob.glob(path_hmi + 'HMI_M_720S_%04d_%02d_%02d_%02d_00_00.fits'%(year, month, day, hour)))
                list_sdo.append(list_hmi)

                for i in range(len(wavelnths)):
                    wavelnth = wavelnths[i]
                    path_aia = '/home/joshua/NAS/AIA/%d/%04d/%02d/%02d/' % (wavelnth, year, month, day)
                    list_aia = sorted(glob.glob(path_aia + 'AIA_%d_%04d_%02d_%02d_%02d_00_*.fits' % (wavelnth, year, month, day, hour)))
                    list_sdo.append(list_aia)

                nbs = [len(list_sdo[n]) for n in range(len(list_sdo))]
                answer = np.prod(np.array(nbs))

                path_target = '/home/joshua/conda_venv/sunpy/euv/SDO/%04d/%02d/%02d/' % (year, month, day)
                list_target = sorted(glob.glob(path_target + 'SDO_%04d_%02d_%02d_%02d_00_00.npy' % (year, month, day, hour)))

                if answer == 1 and len(list_target) == 0 :

                    list_data, list_quality = [], []

                    for j in range(len(list_sdo)):

                        fits = list_sdo[j][0]
                        data, summary = prep_and_resize(fits, isize_target, rsun_target)
                        list_data.append(data)
                        list_quality.append(summary['quality'])

                    if sum(list_quality) == 0 :

                        stacks = np.stack((list_data[k] for k in range(len(list_sdo))), -1)
                        path_save = path_target
                        name_save = 'SDO_%04d_%02d_%02d_%02d_00_00.npy' % (year, month, day, hour)
                        os.makedirs(path_save, mode = 0o777, exist_ok = True)
                        np.save(path_save + name_save, stacks)
                        print(path_save + name_save)


                hour += 1
            day += 1
        month += 1
    year += 1



    
