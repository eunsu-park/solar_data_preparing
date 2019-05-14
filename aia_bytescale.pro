function aia_bytescale, data, wavelnth
  case wavelnth of
    '94': scl = [sqrt((Data * 4.99803)>(1.5)<(50.)), sqrt(1.5), sqrt(50.)]
    '131': scl = [alog10((Data * 6.99685)>(7.0)<(1200.)), alog10(7.0), alog10(1200.)]
    '171': scl = [sqrt((Data * 4.99803)>(10.)<(6000.)), sqrt(10.), sqrt(6000.)]
    '193': scl = [alog10((Data * 2.99950)>(120.)<(6000.)), alog10(120.), alog10(6000.)]
    '211': scl = [alog10((Data * 4.99801)>(30.)<(13000.)), alog10(30.), alog10(13000.)]
    '304': scl = [alog10((Data * 4.99941)>(50.)<(2000.)), alog10(50.), alog10(2000.)]
    '335': scl = [alog10((Data * 6.99734)>(3.5)<(1000.)), alog10(3.5), alog10(1000.)]
    '1600': scl = [(Data * 2.99911)>(0.)<(1000.), 0., 1000.]
    '1700': scl = [(Data * 1.00026)>(0.)<(2500.), 0., 2500.]
    '4500': scl = [(Data * 1.00026)>(0.)<(26000.), 0., 26000.]
  endcase
  return, bytscl(SCL[0], min = SCL[1], max = SCL[1], top = 255)
end
