from sunpy.map import Map
from sunpy.instr.aia import aiaprep
import numpy as np
import glob, os
from imageio import imsave
from tools import hmsm_to_days, date_to_jd, jd_to_date, days_to_hmsm
from sunpy.io import fits

def MAKE_LIST(root_data, year, month, day, hour):
    step = np.arange(21) - 10
    list_data = []
    for n in range(len(step)):
        jd = date_to_jd(year, month, day + hmsm_to_days(hour = hour, min = 0, sec = 0 + 0.001, micro = 0)) + step[n] * 45./86400.
        date = jd_to_date(jd)
        year_c, month_c, day_c = date[0], date[1], int(date[2])
        jd_decimal = date[2] - day_c
        hour_c, minute_c, second_c, _ = days_to_hmsm(jd_decimal)
        path_data = '%s/%04d/%02d/%02d' % (root_data, year_c, month_c, day_c)
        name_data = 'HMI_M_45S_%04d_%02d_%02d_%02d_%02d_%02d.fits' % (year_c, month_c, day_c, hour_c, minute_c, second_c)
        tmp = glob.glob('%s/%s'%(path_data, name_data))
        if len(tmp) > 0 :
            list_data.append(tmp[0])
    return list_data

def MAKE_PATCH(fits_hmi, index):
    map_hmi = aiaprep(Map(fits_hmi))
    data = map_hmi.data
    meta = map_hmi.meta
    shift_index = index - 10
    rsun = meta['r_sun']
    angle = (shift_index*360.*np.pi) / (27.*24.*80.*180.)
    shift_before = rsun * np.sin(angle)
    R = np.around(shift_before)
    I = shift_before
    if abs(R - shift_before) < abs(I - shift_before):
        shift_pixel = int(R)
    else :
        shift_pixel = int(I)
    loc1 = 2048-128
    loc2 = 2048+128
    patch = data[loc1:loc2, loc1+shift_pixel:loc2+shift_pixel]
    return patch, meta

def SAVE_FILES(stacks, center, header, year, month, day, hour, minute, second, path_save):
    path_stacks = '%s/hmi_stacks/%04d/%02d/%02d'%(path_save, c_year, c_month, c_day)
    path_center = '%s/hmi_center/%04d/%02d/%02d'%(path_save, c_year, c_month, c_day)
    os.makedirs(path_stacks, exist_ok=True)
    os.makedirs(path_center, exist_ok=True)
    name_stacks = 'hmi.stacks.%04d.%02d.%02d.%02d.00.00' % (c_year, c_month, c_day, c_hour)
    name_center = 'hmi.center.%04d.%02d.%02d.%02d.00.00' % (c_year, c_month, c_day, c_hour)
    np.save('%s/%s.npy'%(path_stacks, name_stacks), stacks)
    np.save('%s/%s.npy'%(path_center, name_center), center)
    fits.write('%s/%s.fits'%(path_stacks, name_stacks), stacks, header)
    fits.write('%s/%s.fits'%(path_center, name_center), center, header)
    stacks_image = ((stacks.clip(-30, 30)+30.)*(255./60.)).clip(0, 255).astype(np.uint8)
    center_image = ((center.clip(-30, 30)+30.)*(255./60.)).clip(0, 255).astype(np.uint8)
    imsave('%s/%s.png'%(path_stacks, name_stacks), stacks_image)
    imsave('%s/%s.png'%(path_center, name_center), center_image)

def MAKE_PAIRS(root_data, root_save, c_year, c_month, c_day, c_hour, c_minute=0, c_second=0):

    if c_month == 11 :
        path_save = '%s/validation' % root_save
    elif c_month == 12 :
        path_save = '%s/test' % root_save
    else :
        path_save = '%s/train' % root_save

    check_path = '%s/hmi_stacks/%04d/%02d/%02d'%(path_save, c_year, c_month, c_day)
    check_name = 'hmi.stacks.%04d.%02d.%02d.%02d.%02d.%02d.fits' % (c_year, c_month, c_day, c_hour, c_minute, c_second)
    check_list = glob.glob('%s/%s'%(check_path, check_name))

    if len(check_list) == 0 :

        list_hmi = MAKE_LIST(root_data, c_year, c_month, c_day, c_hour)
        if len(list_hmi) == 21 :
            stacks = np.zeros((256, 256))
            for j in range(21):
                patch, header_tmp = MAKE_PATCH(list_hmi[j], index = j)
                print('%s: Index %d/21 of %04d-%02d-%02dT%02d:00:00 ...' % (header_tmp['t_rec'], j+1, c_year, c_month, c_day, c_hour))
                stacks += patch
                if j == 10 :
                    center = patch
                    header = header_tmp
            stacks /= 21.

            SAVE_FILES(stacks, center, header, c_year, c_month, c_day, c_hour, c_minute, c_second, path_save)

root_data = '/DATA/NAS/HMI/M_45S'
root_save = '/userhome/park_e/python_workspace/magnetogram_denoising/datasets'

c_year = 2013
c_month = 1
c_day = 1
c_hour = 0

while c_year < 2014:
    MAKE_PAIRS(root_data, root_save, c_year, c_month, c_day, c_hour)
    jd = date_to_jd(c_year, c_month, c_day + hmsm_to_days(hour = c_hour, min = 0, sec = 0 + 0.001, micro = 0)) + 3600./86400.
    date = jd_to_date(jd)
    c_year, c_month, c_day = date[0], date[1], int(date[2])
    jd_decimal = date[2] - c_day
    c_hour, _, _, _ = days_to_hmsm(jd_decimal)






def test():
    list_hmi = MAKE_LIST(root_data, c_year, c_month, c_day, c_hour)
    stacks = np.zeros((256, 256))
    for j in range(21):
        patch, header_tmp = MAKE_PATCH(list_hmi[j], index = j)
        print('%s: Index %d/21 of %04d-%02d-%02dT%02d:00:00 ...' % (header_tmp['t_rec'], j+1, c_year, c_month, c_day, c_hour))
        stacks += patch
        if j == 10 :
            center = patch
            header = header_tmp
    stacks /= 21.
    np.save('/userhome/park_e/python_workspace/stack_test/result/center_v1.npy', center)
    np.save('/userhome/park_e/python_workspace/stack_test/result/stacks_v1.npy', stacks)













