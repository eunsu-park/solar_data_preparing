from sunpy.net import Fido as F
from sunpy.net.attrs import vso as V
from astropy.time import Time as T
import astropy.units as u
import math
from shutil import move
from tool_date import hmsm_to_days, date_to_jd, jd_to_date, days_to_hmsm, time_hmi

def DownSDO(Instrument, Year, Month, Day, Hour, Minute, Second, path_down, Wave=None, Cadence=None):

    if not Instrument.lower() in ['hmi', 'aia'] :
        raise ValueError("Incorrect instrument {}".format(Instrument))

    if Instrument.lower() == 'hmi':
        if not Cadence in [45, 720] :
            raise ValueError("Incorrect HMI cadence {}".format(Cadence))
        else :
            Type = Instrument.upper() + '_' + str(Cadence)
    else :
        if not Wave in [94, 131, 171, 193, 211, 304, 335, 1600, 1700, 4500] :
            raise ValueError("Incorrect AIA Wavelength {}".format(Wave))
        else :
            Type = Instrument.upper() + '_' + str(Wave)

    Instruments = {'AIA_94':(0, 59), 'AIA_131':(0, 59),
                   'AIA_171':(0, 59), 'AIA_193':(0, 59),
                   'AIA_211':(0, 59), 'AIA_304':(0, 59),
                   'AIA_335':(0, 59), 'AIA_1600':(0, 59),
                   'AIA_1700':(0, 59), 'AIA_4500':(0, 59),
                   'HMI_45':(-90, -45), 'HMI_720':(-300, 300)}

    Catch = Instruments[Type]

    JD = date_to_jd(Year, Month, Day + hmsm_to_days(Hour, Minute, Second, 100))

    JD_S = JD + Catch[0]/86400.
    JD_E = JD + Catch[1]/86400.

    if Instrument.lower() == 'aia' :
        Query = F.search(V.Time(T(JD_S, format = 'jd'), T(JD_E, format = 'jd')),
                         V.Provider('JSOC'), V.Instrument('AIA'),
                         V.Wavelength(int(Wave)*u.angstrom))
    else :
        if Cadence == 45 :
            PO = 'LOS_MAGNETIC_FIELD'
        else :
            PO = 'VECTOR_MAGNETIC_FIELD'
        Query = F.search(V.Time(T(JD_S, format = 'jd'), T(JD_E, format = 'jd')),
                         V.Provider('JSOC'), V.Instrument('HMI'),
                         V.Physobs(PO))
    if Query._numfile > 0 :

        try :
            Fetch = F.fetch(Query[0, 0], path = './')
            move(Fetch[0], path_down)
        except :
            pass

    else :
        print('No file searched, ' + Type)
