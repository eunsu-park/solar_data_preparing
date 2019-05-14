pro sdo_prep_example

fits_sdo = '/home/joshua/HMI_M_720S_2011_12_01_00_00_00.fits'

preped_and_resize = sdo_prep_and_resize(fits_sdo, 1024, 392)
preped = sdo_prep(fits_sdo)

data = preped_and_resize.data>(-100.)<(100.)
tvscl, data

end



