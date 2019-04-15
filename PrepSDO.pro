pro PrepSDO

list_fits = file_search('/home/joshua/github_storage/prep/AIA*fits', count = N)

for i = 0, N-1 do begin

  Fits = list_fits[i]

  SPLIT1 = strsplit(Fits, '/', /extract)
  SPLIT2 = strsplit(SPLIT1[-1], '_', /extract)

  Wavelnth = SPLIT2[1]

  print, Wavelnth

  case Wavelnth of
      '94'  : MaxVal = 900
      '131' : MaxVal = 900
      '171' : MaxVal = 6400
      '193' : MaxVal = 8100
      '211' : MaxVal = 3600
      '304' : MaxVal = 1600
      '335' : MaxVal = 900
      '1600': MaxVal = 3600
      '1700': MaxVal = 10000
    endcase


  read_sdo, Fits, H, D
  B=Main(H, D, 2048, 896)

  RatioAIA = FindRatio(B.datetime, Wavelnth)

  D = D * RatioAIA

  print, minmax(B.data)

  BB = B.data>0<MaxVal
  print, minmax(BB)

  BB = sqrt(BB)
  print, minmax(BB)

  BB = (BB/sqrt(MaxVal))*255.
  print, minmax(BB)

  BB = bytscl(BB)
  print, minmax(BB)

  write_png, '/home/joshua/github_storage/prep/' + string(i, format = '(I4.4)') + '.png', BB

endfor
end

function Main, H, D, Isize, Rsun

  aia_prep, H, D, Header, Data

  TimeRec = Header.T_REC
  Instrument = strmid(Header.INSTRUME, 0, 3)
  Wavelnth = strsplit(fix(Header.WAVELNTH), ' ', /extract)
  Exptime = Header.exptime

  if Instrument eq 'AIA' then begin
    Type_Instr = Wavelnth
    Data = Data / Exptime
  endif else begin
    if Instrument eq 'HMI' then begin
      Type1 = strmid(Header.content, 0, 1)
      Type2 = strsplit(fix(Header.cadence), ' ', /extract) + 'S'
      Type_Instr = Type1 + '_' + Type2
    endif else begin
      message, 'Fits is neither AIA nor HMI'
    endelse
  endelse

  Year = strmid(TimeRec, 0, 4)
  Month = strmid(TimeRec, 5, 2)
  Day = strmid(TimeRec, 8, 2)
  Hour = strmid(TimeRec, 11, 2)
  Minute = strmid(TimeRec, 14, 2)
  Second = strmid(TimeRec, 17, 2)

  DateTime = Year + '_' + Month + '_' + Day + '_' + Hour + '_' + Minute + '_' + Second

  RSunOrig = Header.R_SUN
  ISizeOrig = Header.NAXIS1

  ISizeNew = fix(IsizeOrig * RSun / RSunOrig)
  if ISizeNew mod 2 eq 1 then ISizeNew += 1

  DataCon = congrid(Data, ISizeNew, ISizeNew, /interp, /center)

  PSize = fix((ISize - ISizeNew)/2)
  if PSize gt 0 then begin
    DataPad = make_array(ISize, ISize)
    DataPad[PSize - 1 : PSize + ISizeNew - 2, PSize - 1 : PSize + ISizeNew - 2] = DataCon
  endif else begin
    if PSize lt 0 then begin
      DataPad = DataCon[abs(PSize):ISizeNew-abs(Psize)-1, abs(PSize):ISizeNew-abs(Psize)-1]
    endif else begin
      DataPad = DataCon
    endelse
  endelse

  FileName = Instrument + '_' + Type_Instr + '_' + DateTime + '.png'

  return, {Data:DataPad, DateTime:DateTime, FileName:FileName}

end

function FindRatio, DateTime, Wavelnth
  if Wavelnth eq '1600' or Wavelnth eq '1700' or Wavelnth eq '4500' then begin
    RatioAIA = 1.0
  endif else begin
    DateTimeRef = '2011-01-01T00:00:00'
    SPT = strsplit(DateTime, '_', /extract)
    DateTimeNew = SPT[0]+'-'+SPT[1]+'-'+SPT[2]+'T'+SPT[3]+':'+SPT[4]+':'+SPT[5]
    AIARef = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = DateTimeRef, /silent)
    AIANew = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = DateTimeNew, /silent)
    case Wavelnth of 
      '94': RatioAIA = mean(AIARef.all(*,0) / AIANew.all(*,0))
      '131': RatioAIA = mean(AIARef.all(*,1) / AIANew.all(*,1))
      '171': RatioAIA = mean(AIARef.all(*,2) / AIANew.all(*,2))
      '193': RatioAIA = mean(AIARef.all(*,3) / AIANew.all(*,3))
      '211': RatioAIA = mean(AIARef.all(*,4) / AIANew.all(*,4))
      '304': RatioAIA = mean(AIARef.all(*,5) / AIANew.all(*,5))
      '335': RatioAIA = mean(AIARef.all(*,6) / AIANew.all(*,6))
    endcase
  endelse
  return, RatioAIA
end

function ByteScaleAIA, Data, Wavelnth
  case Wavelnth of
    '94': SCL = [sqrt((Data * 4.99803)>(1.5)<(50.)), sqrt(1.5), sqrt(50.)]
    '131': SCL = [alog10((Data * 6.99685)>(7.0)<(1200.)), alog10(7.0), alog10(1200.)]
    '171': SCL = [sqrt((Data * 4.99803)>(10.)<(6000.)), sqrt(10.), sqrt(6000.)]
    '193': SCL = [alog10((Data * 2.99950)>(120.)<(6000.)), alog10(120.), alog10(6000.)]
    '211': SCL = [alog10((Data * 4.99801)>(30.)<(13000.)), alog10(30.), alog10(13000.)]
    '304': SCL = [alog10((Data * 4.99941)>(50.)<(2000.)), alog10(50.), alog10(2000.)]
    '335': SCL = [alog10((Data * 6.99734)>(3.5)<(1000.)), alog10(3.5), alog10(1000.)]
    '1600': SCL = [(Data * 2.99911)>(0.)<(1000.), 0., 1000.]
    '1700': SCL = [(Data * 1.00026)>(0.)<(2500.), 0., 2500.]
    '4500': SCL = [(Data * 1.00026)>(0.)<(26000.), 0., 26000.]
  endcase
  return, bytscl(SCL[0], min = SCL[1], max = SCL[1], top = 255)
end





