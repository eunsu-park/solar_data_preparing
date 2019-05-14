function aia_find_ratio, t_rec, wavelnth
  if wavelnth eq '1600' or wavelnth eq '1700' or wavelnth eq '4500' then begin
    ratio_aia = 1.0
  endif else begin
    t_ref = '2011-01-01T00:00:00'
    aia_ref = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = t_ref, /silent) 
    aia_rec = aia_get_response(/temp, /dn, /chiantifix, /evenorm, /noblend, timedepend_date = t_rec, /silent)
    case Wavelnth of 
       '94': ratio_aia = mean(aia_ref.all(*,0) / aia_rec.all(*,0))
      '131': ratio_aia = mean(aia_ref.all(*,1) / aia_rec.all(*,1))
      '171': ratio_aia = mean(aia_ref.all(*,2) / aia_rec.all(*,2))
      '193': ratio_aia = mean(aia_ref.all(*,3) / aia_rec.all(*,3))
      '211': ratio_aia = mean(aia_ref.all(*,4) / aia_rec.all(*,4))
      '304': ratio_aia = mean(aia_ref.all(*,5) / aia_rec.all(*,5))
      '335': ratio_aia = mean(aia_ref.all(*,6) / aia_rec.all(*,6))
    endcase
  endelse
  return, ratio_aia
end

