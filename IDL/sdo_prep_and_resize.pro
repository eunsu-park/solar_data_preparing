function sdo_prep_and_resize, fits_sdo=fits_sdo, isize=isize, rsun=rsun, resize=resize

  read_sdo, fits_sdo, header, data
  instr = strmid(header.instrume, 0, 3)
  quality = header.quality

  if keyword_set(resize) then begin
    case instr of
      'AIA': preped = aia_prep_and_resize(header=header, data=data, isize=isize, rsun=rsun, /resize)
      'HMI': preped = hmi_prep_and_resize(header=header, data=data, isize=isize, rsun=rsun, /resize)
      else: message, 'Invalid fits file, this is for HMI or AIA'
    endcase
  endif else begin
    case instr of
      'AIA': preped = aia_prep_and_resize(header=header, data=data)
      'HMI': preped = hmi_prep_and_resize(header=header, data=data)
      else: message, 'Invalid fits file, this is for HMI or AIA'
    endcase
  endelse

  data = preped.data
  header = preped.header
  type_instr = preped.type_instr
  datetime = preped.datetime
  filename = strjoin([instr, type_instr, datetime], '_')

  return, {data:data, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename, quality:quality}

end
