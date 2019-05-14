function aia_prep_and_resize, header, data, isize, rsun

  aia_prep, header, data, header_new, data_new

  t_rec = header.t_rec
  date = strmid(t_rec, 0, 10)
  time = strmid(t_rec, 11, 8)
  datetime = strjoin([strsplit(date, '-', /extract),strsplit(time, ':', /extract)], '_')

  type_instr = wavelnth
  exptime = header.exptime

  ratio_aia = aia_find_ratio(t_rec, wavelnth)
  data = (data*ratio_aia)/exptime

  return, {data:data_pad, header:header, type_instr:type_instr, datetime:datetime}

end
