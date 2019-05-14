function hmi_prep_and_resize, header, data, isize, rsun

  aia_prep, header, data, header_new, data_new

  t_rec = header.t_rec
  date = strmid(t_rec, 0, 10)
  time = strmid(t_rec, 11, 8)
  datetime = strjoin([strsplit(date, '.', /extract),strsplit(time, ':', /extract)], '_')

  type1 = strmid(header.content, 0, 1)
  type2 = strsplit(fix(header.cadence), ' ', /extract) + 'S'
  type_instr = type1 + '_' + type2

end
