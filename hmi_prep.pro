function hmi_prep_and_resize, header, data, isize, rsun

  aia_prep, header, data, header_new, data_new

  t_rec = header.t_rec
  instr = strmid(header.instrume, 0, 3)

  if instr eq 'HMI' then begin
    date = strmid(t_rec, 0, 10)
    time = strmid(t_rec, 11, 8)
    datetime = strjoin([strsplit(date, '.', /extract),strsplit(time, ':', /extract)], '_')
    type1 = strmid(header.content, 0, 1)
    type2 = strsplit(fix(header.cadence), ' ', /extract) + 'S'
    type_instr = type1 + '_' + type2
  endif else begin
    message, string(instr, format='Invalid Instrument: %s, This function is for HMI')
  endelse

  filename = strjoin([instr, type_instr, datetime], '_')
  return, {data:data, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename}

end
