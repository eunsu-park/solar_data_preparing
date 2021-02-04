pro sdo_prep_example

fits_sdo = '/home/joshua/HMI_M_720S_2011_12_01_00_00_00.fits'

;preped = sdo_prep_and_resize(fits_sdo=fits_sdo)
;window, 0, xsize=4096, ysize=4096
;tvscl, preped.data>(-100.)<(100.)

preped_and_resize = sdo_prep_and_resize(fits_sdo=fits_sdo, isize=1024, rsun=392, /resize)
window, 1, xsize=1024, ysize=1024
tvscl, preped_and_resize.data>(-100.)<(100.)


end



