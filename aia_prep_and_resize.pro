function aia_prep_and_resize, header, data, isize, rsun

  aia_prep, header, data, header_new, data_new

  t_rec = header.t_rec
  instr = strmid(header.instrume, 0, 3)

  if instr eq 'AIA' then begin
    date = strmid(t_rec, 0, 10)
    time = strmid(t_rec, 11, 8)
    datetime = strjoin([strsplit(date, '-', /extract),strsplit(time, ':', /extract)], '_')
    type_instr = wavelnth
    exptime = header.exptime
    ratio_aia = aia_find_ratio(t_rec, wavelnth)
    data = (data*ratio_aia)/exptime
  endif else begin
    message, string(instr, format='Invalid Instrument: %s')
  endelse

  rsun_orig = header.r_sun
  isize_orig = header.naxis1

  isize_new = fix(isize_orig * rsun / rsun_orig)
  if isize_new mod 2 eq 1 then isize_new += 1
  data_con = congrid(data, isize_new, isize_new, /interp, /center)

  psize = fix((isize - isize_new)/2.)

  if psize gt 0 then begin
    data_pad = make_array(isize, isize)
    data_pad[psize-1:psize+isize_new-2, psize-1:psize+isize_new-2]=data_con
  endif else begin
    if psize lt 0 then begin
      data_pad = data_con[abs(psize):isize_new-abs(psize)-1, abs(psize):isize_new-abs(psize)-1]
    endif else begin
      data_pad = data_con
    endelse
  endelse

  filename = strjoin([instr, type_instr, datetime], '_')
  return, {data:data_pad, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename}

end
