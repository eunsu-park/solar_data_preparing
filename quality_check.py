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

class quality_bit:
    def __init__(self, instr):
        if type(instr) != str :
            raise TypeError('Keyword "instr" is must be string')
        else :
            if instr.lower() == 'mdi':
                self.quality = mdi_quality
            else :
                raise NameError('%s: Unidentified instrument name\nfor now, only MDI is available'%(instr.upper()))
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
