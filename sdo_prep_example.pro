pro sdo_prep_example

fits_sdo = '***.fits'

read_sdo, fits_sdo, header, data
aia_prep, header, data, header_new, data_new

t_rec = header_new.t_rec
wavelnth = strsplit(fix(header_new.wavelnth), ' ', /extract)
response_ratio = aia_find_ratio(t_rec, wavelnth)

data_compensated = data_new * response_ratio
data_intscale = aia_bytescale(data_intscale, wavelnth)

end



