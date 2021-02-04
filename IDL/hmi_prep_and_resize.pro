function hmi_prep_and_resize, header=header, data=data, isize=isize, rsun=rsun, resize=resize

  aia_prep, header, data, header_new, data_new

  t_rec = header.t_rec
  date = strmid(t_rec, 0, 10)
  time = strmid(t_rec, 11, 8)
  datetime = strjoin([strsplit(date, '.', /extract),strsplit(time, ':', /extract)], '_')

  type1 = strmid(header.content, 0, 1)
  type2 = strsplit(fix(header.cadence), ' ', /extract) + 'S'
  type_instr = type1 + '_' + type2

  if keyword_set(resize) then begin

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
  data_final = data_pad

  endif else begin
    data_final = data
  endelse

  return, {data:data_final, header:header, type_instr:type_instr, datetime:datetime}

end
