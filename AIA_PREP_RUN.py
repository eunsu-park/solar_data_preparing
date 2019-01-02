from SDO_PREP import *
from shutil import move

_wavelnth = int(input('Wavelength?     '))


import glob, os

def ed_dy(_yr, _mo):
    list_31 = [1, 3, 5, 7, 8, 10, 12]
    list_30 = [4, 6, 9, 11]
    if _mo in list_31 :
        result = 31
    elif _mo in list_30 :
        result = 30
    else :
        if _yr%4 == 0:
            result = 29
        else :
            result = 28
    return result

_yr = 2011
while _yr <= 2017 :

#    _path_yr_npy = '/NAS/AIA/NPY_2048_0784/%d/%04d/' % (_wavelnth, _yr)
    _path_yr_png = './PNG_2048_0784/%d/%04d/' % (_wavelnth, _yr)
#    os.mkdir(_path_yr_npy) if not os.path.exists(_path_yr_npy) else None
    os.mkdir(_path_yr_png) if not os.path.exists(_path_yr_png) else None

    _mo = 1
    while _mo <= 12 :

#        _path_mo_npy = _path_yr_npy + '%02d/' % (_mo)
        _path_mo_png = _path_yr_png + '%02d/' % (_mo)
#        os.mkdir(_path_mo_npy) if not os.path.exists(_path_mo_npy) else None
        os.mkdir(_path_mo_png) if not os.path.exists(_path_mo_png) else None

        _dy = 1
        while _dy <= ed_dy(_yr, _mo) :

#            _path_dy_npy = _path_mo_npy + '%02d/' % (_dy)
            _path_dy_png = _path_mo_png + '%02d/' % (_dy)
#            os.mkdir(_path_dy_npy) if not os.path.exists(_path_dy_npy) else None
            os.mkdir(_path_dy_png) if not os.path.exists(_path_dy_png) else None

            _hr = 0
            while _hr <= 23 :

                _list_check = sorted(glob.glob(_path_dy_png + 'AIA_%d_%04d_%02d_%02d_%02d_00_*.png' % (_wavelnth, _yr, _mo, _dy, _hr)))
                if len(_list_check) == 0 :

                    _path = '/NAS/AIA/%d/%04d/%02d/%02d/' % (_wavelnth, _yr, _mo, _dy)
                    _list = sorted(glob.glob(_path + 'AIA_%d_%04d_%02d_%02d_%02d_00_*.fits' % (_wavelnth, _yr, _mo, _dy, _hr)))
                    if len(_list) > 0 :

                        try :
                            _data, _data_bytscl, _summary = prep_and_resize(_list[0], 2048, 784)
                            if _summary['quality'] == 0 :
                                _name = _summary['detector'] + '_' + _summary['type'] + '_' + _summary['date']
#                                np.save(_path_dy_npy + _name + '.npy', _data)
                                imsave(_path_dy_png + _name + '.png', _data_bytscl)
                                print(_list[0], 'Success!')
                            else :
                                print(_list[0], 'Low Quality!')
                        except (TypeError, ValueError, RuntimeError, OSError):
                            move(_list[0], './error/')
                            print(_list[0], 'Error!')
                else :
                    print('AIA_%d_%04d_%02d_%02d_%02d_00_*.png exists' % (_wavelnth, _yr, _mo, _dy, _hr))

                _hr += 1
            _dy += 1
        _mo += 1
    _yr += 1

