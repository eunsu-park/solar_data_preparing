pro PrepSDO

root_data = '/home/joshua/NAS/'
root_save = '/home/joshua/github_storage/datasets/'

;read, instr, prompt = 'AIA or HMI?     '

root_sdo = root_data + 'HMI'
save_sdo = root_save + 'HMI'

;root_aia = root_data + 'AIA'
;root_hmi = root_data + 'HMI'

;save_aia = root_save + 'AIA'
;save_hmi = root_save + 'HMI'

;read, wavelnth, prompt = 'Wavelength?     '

catch, err
if err ne 0 then begin
  catch, /cancel
  goto, skip
endif

year = 2017
while year le 2017 do begin

  month = 1
  while month le 12 do begin

    day = 1
    while day le 31 do begin

      hour = 0
      while hour le 23 do begin

;        path_load = string(root_sdo, wavelnth, year, month, day, format = '%s/%d/%04d/%02d/%02d')
;        path_save = string(save_sdo, wavelnth, year, month, day, format = '%s/%d/%04d/%02d/%02d')
;        file_load = string(path_load, wavelnth, year, month, day, hour, format = '%s/AIA_%d_%04d_%02d_%02d_%02d_00_*.fits')
;        list_load = file_search(file_load, count = nn)
;        list_save = file_search(string(path_save, wavelnth, year, month, day, hour, format = '%s/AIA_%d_%04d_%02d_%02d_%02d_00_*.fits'), count = mm)

        path_load = string(root_sdo, year, month, day, format = '%s/M_720S/%04d/%02d/%02d')
        path_save = string(save_sdo, year, month, day, format = '%s/M_720S/%04d/%02d/%02d')
        file_load = string(path_load, year, month, day, hour, format = '%s/HMI_M_720S_%04d_%02d_%02d_%02d_00_*.fits')
        list_load = file_search(file_load, count = nn)
        list_save = file_search(string(path_save, year, month, day, hour, format = '%s/HMI_M_720S_%04d_%02d_%02d_%02d_00_*.fits'), count = mm)




        if nn gt 0 and mm eq 0 then begin

          fits = list_load[0]
          read_sdo, fits, H, D, /noshell, /uncomp_delete
          if fix(H.quality) eq 0 then begin


            preped = main(H, D, 2048, 896)

            catch, /cancel
            
            file_mkdir, path_save
            name_save = string(path_save, preped.filename, format = '%s/%s.fits')

            print, name_save
            data = float(preped.data)
            head_struct = preped.header
            head_str = struct2fitshead(head_struct)
            help, head_str
            writefits, name_save, data, head_str


          endif
        endif

        skip : print, 'Error!'

        hour += 6
      endwhile
      day += 1
    endwhile
    month += 1
  endwhile
  year += 1
endwhile

print, root_aia, root_hmi

;list_fits = file_search('/home/joshua/github_storage/prep/AIA*fits', count = N)

;for i = 0, 0 do begin

;  fits = list_fits[i]

;  read_sdo, fits, H, D
;  if fix(H.quality) eq 0 then begin

;    preped = main(H, D, 2048, 896)

;    data = preped.data
;    writefits, '/home/joshua/github_storage/' + preped.filename + '.fits', data, header


;  endif




;stop

;restore, fname, /verb


;  SPLIT1 = strsplit(Fits, '/', /extract)
;  SPLIT2 = strsplit(SPLIT1[-1], '_', /extract)
;  Wavelnth = SPLIT2[1]
;  print, Wavelnth
;  case Wavelnth of
;      '94'  : MaxVal = 900
;      '131' : MaxVal = 900
;      '171' : MaxVal = 6400
;      '193' : MaxVal = 8100
;      '211' : MaxVal = 3600
;      '304' : MaxVal = 1600
;      '335' : MaxVal = 900
;      '1600': MaxVal = 3600
;      '1700': MaxVal = 10000
;    endcase




 ; B=

;  print, minmax(B.data)

;  BB = B.data>0<MaxVal
;  print, minmax(BB)

;  BB = sqrt(BB)
;  print, minmax(BB)

;  BB = (BB/sqrt(MaxVal))*255.
;  print, minmax(BB)

;  BB = bytscl(BB)
;  print, minmax(BB)

;  

;endfor
end

function main, H, D, isize, rsun

  aia_prep, H, D, header, data

  t_rec = header.t_rec
  instr = strmid(header.instrume, 0, 3)


  if instr eq 'AIA' then begin

    date = strmid(t_rec, 0, 10)
    time = strmid(t_rec, 11, 8)
    datetime = strjoin([strsplit(date, '-', /extract),strsplit(time, ':', /extract)], '_')

    wavelnth = strsplit(fix(header.wavelnth), ' ', /extract)
    type_instr = wavelnth
    exptime = header.exptime
    ratio_aia = find_ratio(t_rec, wavelnth)
    data = (data*ratio_aia)/exptime
    
  endif else begin
    if instr eq 'HMI' then begin

      date = strmid(t_rec, 0, 10)
      time = strmid(t_rec, 11, 8)
      datetime = strjoin([strsplit(date, '.', /extract),strsplit(time, ':', /extract)], '_')

      type1 = strmid(header.content, 0, 1)
      type2 = strsplit(fix(header.cadence), ' ', /extract) + 'S'
      type_instr = type1 + '_' + type2
    endif else begin
      message, 'Fits is neither AIA nor HMI'
    endelse
  endelse

  data_pad = data

;  rsun_orig = header.r_sun
;  isize_orig = header.naxis1

;  isize_new = fix(isize_orig * rsun / rsun_orig)
;  if isize_new mod 2 eq 1 then isize_new += 1
;  data_con = congrid(data, isize_new, isize_new, /interp, /center)

;  psize = fix((isize - isize_new)/2.)

;  if psize gt 0 then begin
;    data_pad = make_array(isize, isize)
;    data_pad[psize-1:psize+isize_new-2, psize-1:psize+isize_new-2]=data_con
;  endif else begin
;    if psize lt 0 then begin
;      data_pad = data_con[abs(psize):isize_new-abs(psize)-1, abs(psize):isize_new-abs(psize)-1]
;    endif else begin
;      data_pad = data_con
;    endelse
;  endelse

  filename = strjoin([instr, type_instr, datetime], '_')

  return, {data:data_pad, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename}

end

function find_ratio, t_rec, wavelnth
  if wavelnth eq '1600' or wavelnth eq '1700' or wavelnth eq '4500' then begin
    ratio_aia = 1.0
  endif else begin
    t_ref = '2011-01-01T00:00:00'
    aia_ref = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = t_ref, /silent) 
    aia_rec = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = t_rec, /silent)
    case Wavelnth of 
       '94': ratio_aia = mean(aia_ref.all(*,0) / aia_rec.all(*,0))
      '131': ratio_aia = mean(aia_ref.all(*,1) / aia_rec.all(*,1))
      '171': ratio_aia = mean(aia_ref.all(*,2) / aia_rec.all(*,2))
      '193': ratio_aia = mean(aia_ref.all(*,3) / aia_rec.all(*,3))
      '211': ratio_aia = mean(aia_ref.all(*,4) / aia_rec.all(*,4))
      '304': ratio_aia = mean(aia_ref.all(*,5) / aia_rec.all(*,5))
      '335': ratio_aia = mean(aia_ref.all(*,6) / aia_rec.all(*,6))
    endcase
  endelse
  return, ratio_aia
end

function bytescale_aia, data, wavelnth
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





