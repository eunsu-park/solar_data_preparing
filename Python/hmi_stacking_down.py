from sunpy.net import Fido, attrs
from sunpy.net.attrs import vso
from astropy.time import Time
import astropy.units as u
import os, time

root_hmi = '/nas/obsdata/sdo/hmi/M_45s'

root_save = '/userhome/park_e/Datasets/hmi_denoising'
year = 2011
month = 1
day = 1
hour = 7

date = '%04d-%02d-%02dT%02d:00:00.000'%(year, month, day, hour)
date_end = '%04d-%02d-31T23:59:59.999'%(year, month)
date = Time(date)
date_end = Time(date_end)

nb_stack = 21
step = range(nb_stack)# - nb_stack//2
step = [step[n]  - nb_stack//2 for n in range(nb_stack)]

def from_date(date):
    date = date.to_value('fits')
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    minute = date[14:16]
    second = date[17:19]
    return year, month, day, hour, minute, second

def hmi_query(date):
    t_start = date + step[0] * 45./86400. - 90./86400.
    t_end = date + step[-1] * 45./86400. - 45./86400.

    query = Fido.search(attrs.Time(t_start, t_end),
                        attrs.Provider('JSOC'),
                        attrs.Instrument('HMI'),
                        attrs.Physobs('LOS_MAGNETIC_FIELD'))
    return query

while date < date_end :

    q = hmi_query(date)
    if q.file_num == nb_stack :
        print(q)

        year, month, day, hour, minute, second = from_date(date)
        path_save = '%s/%s/%s/%s/%s'%(root_save, year, month, day, hour)
        if not os.path.exists(path_save):
            os.makedirs(path_save)

        f = Fido.fetch(q, path='%s/{file}'%(path_save), progress=False)
        e = f.errors
        while len(e) > 0 :
            f = Fido.fetch(f, progress=False)
            e = f.errors

    date += 1./24.
    time.sleep(60)
            
            


    


#while date < date_end :

#    list_exist = []

#    for n in range(nb_stack):
#        date_tmp = date + step[n] * 45./86400.
#        year, month, day, hour, minute, second = from_date(date_tmp)
#        path = pattern_path%(root_hmi, year, month, day)
#        name = pattern_name%(year, month, day, hour, minute, second)
#        exist = os.path.exists('%s/%s'%(path, name))
#        list_exist.append(exist)

#    year, month, day, hour, minute, second = from_date(date)
#    print('%s-%s-%s-%s-%s-%s : %d'%(year, month, day, hour, minute, second, sum(list_exist)))

#    date += 1./24.






#root_hmi = '/nas/obsdata/sdo/hmi/M_45s'

#root_save = '/userhome/park_e/Datasets/hmi_denoising'
#year = 2011

#path_save = %04d'%(year)

#date = '2011-01-01T00:00:00.000'
#date_end = '2011-12-31T23:59:59.999'
#date = Time(date)
#date_end = Time(date_end)

#nb_stack = 21
#step = range(nb_stack)# - nb_stack//2
#step = [step[n]  - nb_stack//2 for n in range(nb_stack)]

#pattern_path = '%s/%s/%s/%s'
#pattern_name = 'hmi.M_45s.%s-%s-%s-%s-%s-%s.fits'

#def from_date(date):
#    date = date.to_value('fits')
#    year = date[0:4]
#    month = date[5:7]
#    day = date[8:10]
#    hour = date[11:13]
#    minute = date[14:16]
#    second = date[17:19]
#    return year, month, day, hour, minute, second

#def hmi_query(t_start, t_end, physobs):
#    query = Fido.search(attrs.Time(t_start, t_end),
#                        attrs.Provider('JSOC'),
#                        attrs.Instrument('HMI'),
#                        attrs.Physobs(physobs))
#    return query


#while date < date_end :

#    list_exist = []

#    for n in range(nb_stack):
#        date_tmp = date + step[n] * 45./86400.
#        year, month, day, hour, minute, second = from_date(date_tmp)
#        path = pattern_path%(root_hmi, year, month, day)
#        name = pattern_name%(year, month, day, hour, minute, second)
#        exist = os.path.exists('%s/%s'%(path, name))
#        list_exist.append(exist)

#    year, month, day, hour, minute, second = from_date(date)
#    print('%s-%s-%s-%s-%s-%s : %d'%(year, month, day, hour, minute, second, sum(list_exist)))

#    date += 1./24.



#    jd_start = date_start.to_value('jd')



        # for n in range(self.nb_stack):
        #     jd = date_to_jd(year, month, day + hmsm_to_days(hour = hour, min = 0, sec = 0 + 0.001, micro = 0)) + step[n] * 45./86400.
        #     date = jd_to_date(jd)
        #     year_c, month_c, day_c = date[0], date[1], int(date[2])
        #     jd_decimal = date[2] - day_c
        #     hour_c, minute_c, second_c, _ = days_to_hmsm(jd_decimal)
        #     path_ = '%s/%04d/%02d/%02d' % (self.root_hmi, year_c, month_c, day_c)
        #     name_ = 'hmi.M_45s.%04d-%02d-%02d-%02d-%02d-%02d.fits' % (year_c, month_c, day_c, hour_c, minute_c, second_c)
        #     tmp = glob('%s/%s'%(path_, name_))
        #     if len(tmp) > 0 :
        #         list_tmp.append(tmp[0])








#t_start = '2011-01-01T00:00:00.000'
#t_end = '2011-01-01T00:00:45.000'

#jd_start = Time(t_start)
#jd_end = Time(t_end)

#jd_start.format = 'jd'# 'fits'
#jd_end.format = 'jd' # 'fits'

#print(jd_start.value)
#print(jd_end.value)

#physobs = 'LOS_MAGNETIC_FIELD'

#q = hmi_query(t_start, t_end, physobs)
