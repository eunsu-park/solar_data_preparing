from sunpy.net import Fido, attrs
from sunpy.net.attrs import vso
from astropy.time import Time
import astropy.units as u

def hmi_query(t_start, t_end, physobs):
    query = Fido.search(attrs.Time(t_start, t_end),
                        attrs.Provider('JSOC'),
                        attrs.Instrument('HMI'),
                        attrs.Physobs(physobs))
    return query

def aia_query(t_start, t_end, wavelength):
    query = Fido.search(attrs.Time(t_start, t_end),
                        attrs.Provider('JSOC'),
                        attrs.Instrument('AIA'),
                        attrs.Wavelength(wavelength*u.angstrom))
    return query



t_start = '2011-01-01T00:00:00.000'
t_end = '2011-01-01T00:00:45.000'

jd_start = Time(t_start)
jd_end = Time(t_end)

jd_start.format = 'jd'# 'fits'
jd_end.format = 'jd' # 'fits'

print(jd_start.value)
print(jd_end.value)

physobs = 'LOS_MAGNETIC_FIELD'

q = hmi_query(t_start, t_end, physobs)