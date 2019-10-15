"""
for standard mdi quality bit, http://soi.stanford.edu/production/QUALITY/DATASWtable.html
and mdi M_96m quality bit, http://soi.stanford.edu/production/QUALITY/bits.fd_M.html
"""
mdi_quality = {'0':'Any telemetry problem/missing',
                '1':'T_OBS Missing',
                '2':'>0 Missing',
                '3':'>0.01 Missing',
                '4':'>0.1 Missing',
                '5':'>0.5 Missing',
                '6':'>0.9 Missing',
                '7':'On-board Processing Error',
                '8':'Pointing Anomaly',
                '9':'MDI is NOT in PRIME 60',
                '10':'Cosmic Rays',
                '11':'Statistics unlikely',
                '16':'Telemetry Dropout',
                '17':'Structure Program Problem',
                '18':'Stored Magnetogram Corruption',
                '19':'Minor Image Fragment OK',
                '20':'Major Image Fragment OK',
                '21':'Data Statistics Problem',
                '28':'Override',
                '29':'Warning',
                '30':'DATA BAD',
                '31':'??'}

"""
for SDO AIA and HMI level 1 quality bit, http://jsoc.stanford.edu/~jsoc/keywords/AIA/AIA02840_K_AIA-SDO_FITS_Keyword_Document.pdf
"""
sdo_quality = {'0':'FLAT_REC == MISSING',
                '1':'ORB_REC == MISSING',
                '2':'ASD_REC == MISSING',
                '3':'MPO_REC == MISSING',
                '4':'RSUN_LF == MISSING or X0_LF == MISSING or Y0_LF == MISSING',
                '8':'MISSVALS > 0',
                '9':'MISSVALS > 0.01*TOTVALS',
                '10':'MISSVALS > 0.05*TOTVALS',
                '11':'MISSVALS > 0.25*TOTVALS',
                '12':'ACS_MODE != "SCIENCE"',
                '13':'ACS_ECLP == "YES"',
                '14':'ACS_SUNP == "NO"',
                '15':'ACS_SAFE == "YES"',
                '16':'IMG_TYPE == "DARK"',
                '17':'HWLTNSET == "OPEN" or AISTATE == "OPEN"',
                '18':'(FID >= 1 and FID <= 9999) or (AIFTSID >= 0xC000)',
                '19':'HCFTID == 17',
                '20':'(AIFCPS <= -20 or AIFCPS >= 100)',
                '21':'AIAGP6 != 0',
                '30':'Quicklook image',
                '31':'Image not available'}

class quality_bit:
"""
print error bit and error code
This class will work for MDI level 1.5, and SDO (AIA and HMI) level 1 quality bit
"""

    def __init__(self, instr):
        if type(instr) != str :
            raise TypeError('Keyword "instr" is must be string')
        else :
            if instr.lower() == 'mdi':
                self.quality = mdi_quality
            elif instr.lower() in ['hmi', 'aia', 'sdo']:
                self.quality = sdo_quality
            else :
                raise NameError('%s: Unidentified instrument name\nfor now, only MDI, SDO(AIA and HMI) is available'%(instr.upper()))
    def __call__(self, q):
        h = int(q, 16)
        b = bin(h)
        l = len(b) - 2
        n = 1
        list_bit = []
        list_problem = []
        while n <= l :
            bit = b[-n]
            if int(bit) == 1 :
                if str(n-1) in self.quality :
                    list_bit.append(int(n-1))
                    list_problem.append(self.quality[str(n-1)])
                else :
                    list_bit.append(int(n-1))
                    list_problem.append('Unidentified bit')
            n += 1
        return list_bit, list_problem
