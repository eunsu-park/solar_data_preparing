import numpy as np
from sunpy.map import Map
from skimage.transform import resize
from sunpy.instr.aia import aiaprep
from numba import jit
from imageio import imsave
from scipy.misc import bytescale



@jit
def aia_bytescale(_data, _wavelnth):

    _bytscls = {  '94' : (4.99803,  1.5,    50.),
                 '131' : (6.99685,  7.0,  1200.),
                 '171' : (4.99803,  10.,  6000.),
                 '193' : (2.99950, 120.,  6000.),
                 '211' : (4.99801,  30., 13000.),
                 '304' : (4.99941,  50.,  2000.),
                 '335' : (6.99734,  3.5,  1000.),
                '1600' : (2.99911,   0.,  1000.),
                '1700' : (1.00026,   0.,  2500.),
                '4500' : (1.00026,   0., 26000.)}

    _logs = [131, 193, 211, 304, 335]
    _sqrts = [94, 171]
    _lins = [1600, 1700, 4500]
    _bytscl = _bytscls[str(_wavelnth)]
    _bytscl_factor, _bytscl_min, _bytscl_max = _bytscl

    _data *= _bytscl_factor

    _data_new = np.where(_data > _bytscl_max, _bytscl_max, _data)
    _data_new = np.where(_data < _bytscl_min, _bytscl_min, _data_new)

    if _wavelnth in _logs :
        _data_bytscl = bytescale(np.log10(_data_new), cmin = np.log10(_bytscl_min), cmax = np.log10(_bytscl_max), high = 255, low = 0)
    elif _wavelnth in _sqrts :
        _data_bytscl = bytescale(np.sqrt(_data_new), cmin = np.sqrt(_bytscl_min), cmax = np.sqrt(_bytscl_max), high = 255, low = 0)
    elif _wavelnth in _lins :
        _data_bytscl = bytescale(_data_new, cmin = _bytscl_min, cmax = _bytscl_max, high = 255, low = 0)
    else :
        raise TypeError('Incorrect Wavelength!')

    return _data_bytscl

@jit
def hmi_bytescale(_data, _min = -100, _max = 100) :
    _data_new = np.where(_data > _max, _max, _data)
    _data_new = np.where(_data < _min, _min, _data_new)
    _data_bytscl = bytescale(_data_new, cmin = _min, cmax = _max, high = 255, low = 0)
    return _data_bytscl

@jit
def hmi_cutting(_data_hmi, _isize, _rsun):
    _data_hmi_new = np.where(np.isnan(_data_hmi), np.nanmin(_data_hmi), _data_hmi)
    for i in range(_isize):
        for j in range(_isize):
            if (i-_isize/2.)**2. + (j-_isize/2.)**2. > _rsun ** 2. :
                _data_hmi_new[i, j] = -5000
    return _data_hmi_new

def find_ratio(_wavelnth, _yr, _mo, _dy, _hr):

    _time_format = '%04d-%02d-%02dT%02d:00:00' % (_yr, _mo, _dy, _hr)
    _read = open('./ratios/ratio_aia_%d_%04d.txt' % (_wavelnth, _yr), 'r')
    for _line in _read.readlines():
        _date = _line[0:19]
        if _date == _time_format :
            _ratio = float(_line[19:])
            break
   
    return _ratio

@jit
def prep_and_resize(_file, _isize_target, _rsun_target):

    _map = Map(_file)

    _detector = _map.meta['detector']
    _wavelnth = _map.meta['wavelnth']
    _quality = _map.meta['quality']
    _t_rec = _map.meta['t_rec']

    if _detector == 'AIA':
        _type = str(_wavelnth)

    elif _detector == 'HMI' :
        _type1 = _map.meta['content'][0]
        _type2 = str(int(_map.meta['cadence'])) + 'S'
        _type = _type1 + '_' + _type2

    else :
        raise NameError('File is neither AIA nor HMI')

    _date = _t_rec[0:4] + '_' + _t_rec[5:7] + '_' + _t_rec[8:10] + '_' + _t_rec[11:13] + '_' + _t_rec[14:16] + '_' + _t_rec[17:19]
    _yr, _mo, _dy, _hr, _mn, _sc = np.array([_t_rec[0:4], _t_rec[5:7], _t_rec[8:10], _t_rec[11:13], _t_rec[14:16], _t_rec[17:19]], dtype = np.int)


    if _quality == 0 :

        _map_prep = aiaprep(_map)
        _meta = _map_prep.meta
        _rsun = _meta['r_sun']
        _isize = _meta['naxis1']

        if _detector == 'AIA' :    
            if _wavelnth in [94, 131, 171, 193, 211, 304, 335] :
                _ratio = find_ratio(_wavelnth, _yr, _mo, _dy, _hr)
                _data = _map_prep.data * _ratio / _meta['exptime']
            else :
                _data = _map_prep.data / _meta['exptime']
        elif _detector == 'HMI' :
            _data = _map_prep.data
        else :
            raise NameError('File is neither AIA nor HMI')

        _isize_mid = int(_isize * _rsun_target / _rsun)
        _isize_mid = int(_isize * _rsun_target / _rsun)
        if _isize_mid % 2 != 0 :
            _isize_mid += 1 

        _pocsize = (_isize_target - _isize_mid)//2
        _data_mid = resize(_data, (_isize_mid, _isize_mid), order = 1, mode = 'constant', preserve_range = True)

        if _pocsize > 0 :
            _data_new = np.flipud(np.pad(_data_mid, _pocsize, mode = 'constant'))
        elif _picsize < 0 :    
            _data_new = np.flipud(_data_mid[_pocsize:-_pocsize, _pocsize:-_pocsize])
        else :
            _data_new = _data_mid

        if _detector == 'AIA':
            _data_bytscl = aia_bytescale(_data_new, _wavelnth)

        elif _detector == 'HMI' :
            _data_new = hmi_cutting(_data_new, _isize_target, _rsun_target)
            _data_bytscl = hmi_bytescale(_data_new)
        else :
            raise NameError('File is neither AIA nor HMI')

    else :
        _data_new = None
        _data_bytscl = None

    _summary = {'date':_date, 'detector':_detector, 'type':_type, 'quality':_quality}
    
    return _data_new, _data_bytscl, _summary






