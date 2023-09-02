#### 
input_dir = 'data/cloudA'
filename_12m7mtp = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_single'
filename_12m7m = f'{input_dir}/cloudA_12m+7m_n2hp10_single'
filename_tp = f'{input_dir}/cloudA_tp_n2hp10_single'
####

################## Run tclean 
print('[INFO] Creating 12m+7m tclean dirty image')

os.system('rm -rf %s_tclean_dirty*'%filename_12m7m)
os.system('rm -rf %s_tclean*'%filename_12m7m)

tclean(vis=['%s.ms' %filename_12m7m], 
       imagename='%s_tclean_dirty'%filename_12m7m,
       cell=['0.5arcsec'], 
       imsize=[360, 250],
       restoringbeam='common',
       phasecenter='ICRS 18:26:18.2934 -012.41.27.253',
       stokes='I', 
       specmode='cube', 
       outframe='LSRK',
       nchan=1,
       start=1,
       width=1,
       gridder='mosaic', 
       usepointing=False, 
       mosweight=True,
       pblimit=0.2,
       deconvolver='hogbom', 
       pbcor=False,
       weighting='briggs',
       robust=2.0,
       niter=0)

tclean(vis=['%s.ms' %filename_12m7m],
       imagename='%s_tclean'%filename_12m7m,
       cell=['0.5arcsec'], 
       imsize=[360, 250],
       restoringbeam='common',
       phasecenter='ICRS 18:26:18.2934 -012.41.27.253',
       stokes='I', 
       specmode='cube', 
       outframe='LSRK',
       nchan=1,
       start=1,
       width=1,
       gridder='mosaic', 
       usepointing=False, 
       mosweight=True,
       pblimit=0.2,
       deconvolver='hogbom', 
       pbcor=True,
       weighting='briggs',
       robust=2.0,
       niter=600000, 
       threshold='0.03Jy',
       usemask='auto-multithresh',
       sidelobethreshold=2.0,
       noisethreshold=4.25,
       lownoisethreshold=1.5, 
       negativethreshold=0,
       minbeamfrac=0.3,
       growiterations=50, 
       minpercentchange=1.0)

################## Prep SD 
print('[INFO] Preparing single dish data...')

importfits(fitsimage='%s.fits'%filename_tp,
       imagename='%s.image'%filename_tp,
       overwrite=True)

print('[INFO] Updating single dish header')
imhead(imagename='%s.image'%filename_tp, 
       mode='put', 
       hdkey='telescope', 
       hdvalue='ALMA')

print('[INFO] Regridding single dish to dirty image')
imregrid(imagename='%s.image'%filename_tp,
       template='%s_tclean_dirty.image'%filename_12m7m,
       asvelocity=False,
       overwrite=True,
       output='%s_regrid.image'%filename_tp)

os.system('rm -rf %s_regrid_trans.image'%filename_tp)
imtrans(imagename='%s_regrid.image'%filename_tp,
       outfile='%s_regrid_trans.image'%filename_tp,
       order=['rig', 'declin', 'stok', 'frequ'])

################## Feather SD to tclean
print('[INFO] Feathering single dish data...')

os.system('rm -rf %s_tcleanfeather.image'%filename_12m7mtp)

feather(imagename='%s_tcleanfeather.image'%filename_12m7mtp,
       highres='%s_tclean.image.pbcor'%filename_12m7m, 
       lowres='%s_regrid_trans.image'%filename_tp)

exportfits(imagename='%s_tcleanfeather.image'%filename_12m7mtp,
       fitsimage='%s_tcleanfeather.image.fits'%filename_12m7mtp,
       velocity=True,
       overwrite=True)

################## Run sdintimaging
print('[INFO] Running sdintimaging...')

os.system('rm -rf %s_sdintimaging*' %filename_12m7mtp)
sdimage='%s_regrid_trans.image'%filename_tp

sdintimaging(usedata='sdint',
              sdimage=sdimage,
              sdpsf='',
              sdgain=1.0,
              dishdia=12.0,
              vis=['%s.ms' %filename_12m7m],
              imagename='%s_sdintimaging'%filename_12m7mtp,
              cell=['0.5arcsec'], 
              imsize=[360, 250],
              restoringbeam='common',
              phasecenter='ICRS 18:26:18.2934 -012.41.27.253',
              stokes='I', 
              specmode='cube', 
              outframe='LSRK',
              nchan=1,
              start=1,
              width=1,
              gridder='mosaic', 
              usepointing=False, 
              mosweight=True,
              pblimit=0.2,
              deconvolver='hogbom', 
              pbcor=True,
              weighting='briggs',
              robust=2.0,
              niter=600000, 
              threshold='0.03Jy',
              usemask='auto-multithresh',
              sidelobethreshold=2.0,
              noisethreshold=4.25,
              lownoisethreshold=1.5, 
              negativethreshold=0,
              minbeamfrac=0.3,
              growiterations=50, 
              minpercentchange=1.0) 

print('[INFO] Exporting to .fits')
exportfits(imagename='%s_sdintimaging.joint.cube.image.pbcor'%filename_12m7mtp,
       fitsimage='%s_sdintimaging.joint.cube.image.pbcor.fits'%filename_12m7mtp,
       velocity=True,
       overwrite=True)