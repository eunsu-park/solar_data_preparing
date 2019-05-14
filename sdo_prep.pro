function sdo_prep, fits

  read_sdo, fits, header, data
  instr = strmid(header.instrume, 0, 3)
  quality = header.quality

  case instr of

    'AIA': preped = aia_prep(header, data)
    'HMI': preped = hmi_prep(header, data)
    else: message, 'Invalid fits file, this is for HMI or AIA'

  endcase

  data = preped.data
  header = preped.header
  type_instr = preped.type_instr
  datetime = preped.datetime
  filename = strjoin([instr, type_instr, datetime], '_')

  return, {data:data, header:header, instr:instr, type_instr:type_instr, datetime:datetime, filename:filename, quality:quality}

end
