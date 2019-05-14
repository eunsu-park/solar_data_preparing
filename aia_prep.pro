function aia_prep, header, data

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

  filename = strjoin([instr, type_instr, datetime], '_')
  return, {data:data, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename}

end
