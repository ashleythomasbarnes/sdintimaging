
####
input_dir = 'data/cloudA'
filename_12m7m = f'{input_dir}/cloudA_12m+7m_n2hp10'
filename_12m7m_single = f'{input_dir}/cloudA_12m+7m_n2hp10_single'
filename_tp = f'{input_dir}/cloudA_tp_n2hp10'
####

##################

importfits(fitsimage='%s.fits'%filename_tp,
      imagename='%s.image'%filename_tp,
      overwrite=True)

imregrid(imagename='%s.image'%filename_tp,
      template='%s_tclean.image'%filename_12m7m,
      asvelocity=False,
      overwrite=True,
      output='%s_regrid.image'%filename_tp)

imsubimage(imagename='%s_regrid.image'%filename_tp,
            outfile='%s_single.image'%filename_tp,
            chans='24',
            overwrite=True)

exportfits(imagename='%s_single.image'%filename_tp,
      fitsimage='%s_single.fits'%filename_tp,
      velocity=True,
      overwrite=True)
##################