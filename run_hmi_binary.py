

isize_target = 1024
rsun_target = 392

from prep_sdo import * #prep_and_resize
import glob, os
import numpy as np
from shutil import move

year = 2011
while year <= 2017 :

    month = 1
    while month <= 12 :

        day = 1
        while day <= 31 :

            hour = 0
            while hour <= 23 :

                path_load = '/home/joshua/NAS/HMI/M_720S/%04d/%02d/%02d/' % (year, month, day)
                list_load = sorted(glob.glob(path_load + 'HMI_M_720S_%04d_%02d_%02d_%02d_00_*.fits' % (year, month, day, hour)))

                path_target = '/home/joshua/conda_venv/sunpy/euv/datasets/HMI_M_720S/%04d/%02d/%02d/' % (year, month, day)
                list_target = sorted(glob.glob(path_target + 'HMI_M_720S_%04d_%02d_%02d_%02d_00_*.npy' % (year, month, day, hour)))

                if len(list_load) > 0 and len(list_target) == 0:

                    fits = list_load[0]
                    data, summary = prep_and_resize(fits, isize_target, rsun_target)

                    if data is not None :

                        name = summary['detector'] + '_' + summary['type'] + '_' + summary['date'] + '.npy'
                        path_save = './datasets/HMI_M_720S/%04d/%02d/%02d/' % (year, month, day)
                        os.makedirs(path_save, mode = 0o777, exist_ok = True)
                        np.save(path_save + name, data)
                        print(path_save + name, summary)

                hour += 1
            day += 1
        month += 1
    year += 1



    
