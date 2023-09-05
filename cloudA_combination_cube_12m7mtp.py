#### 
input_dir = 'data/cloudA'
filename_12m7mtp = f'{input_dir}/cloudA_12m+7m+tp_n2hp10'
filename_12m7m = f'{input_dir}/cloudA_12m+7m_n2hp10'
filename_tp = f'{input_dir}/cloudA_tp_n2hp10'

filename_12m7mtp_tclean = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_tcleanfeather.image'
filename_12m7mtp_sdint = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_sdintimaging.joint.cube.image.pbcor'
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
       nchan=50,
       start=25,
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
       nchan=50,
       start=25,
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
              nchan=50,
              start=25,
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

################## Run stats
print('[INFO] Running stats...')

for file in [filename_12m7mtp_sdint, filename_12m7mtp_tclean]:
       
       print(f'[INFO] Importing {file}')

       importfits(fitsimage='%s.fits'%file,
                            imagename='%s'%file,
                            overwrite=True)

os.system('rm -rf %s.rms'%filename_12m7mtp_sdint)
immoments(imagename='%s'%filename_12m7mtp_sdint,
                     moments=6,
                     chans='0~11,39~49',
                     outfile='%s.rms'%filename_12m7mtp_sdint)

os.system('rm -rf %s/immath_diff1.image'%input_dir)
immath(imagename=[filename_12m7mtp_tclean, 
                                   filename_12m7mtp_sdint, 
                                   '%s.rms'%filename_12m7mtp_sdint],
              outfile='%s/immath_diff1.image'%input_dir,
              expr='(IM1-IM0)/iif((IM1/IM2)>50,IM1,100000)')

os.system('rm -rf %s/immath_diff2.image'%input_dir)
immath(imagename=[filename_12m7mtp_tclean, 
                                   filename_12m7mtp_sdint, 
                                   '%s.rms'%filename_12m7mtp_sdint],
              outfile='%s/immath_diff2.image'%input_dir,
              expr='abs((IM1-IM0)/IM2)')

stats_diff1 = imstat(imagename='%s/immath_diff1.image'%input_dir)
stats_diff2 = imstat(imagename='%s/immath_diff2.image'%input_dir)

if stats_diff1['max'][0]>0.3: 
       check1 = False
       print('[WARNING] Emission peaks >30 percent different between tclean and sdintclean')
else: 
       check1 = True
       print('[INFO] Emission peaks <30 percent different between tclean and sdintclean')

if stats_diff2['mean'][0]>0.3: 
       check2 = False
       print('[WARNING] Emission mean >3 sigma different between tclean and sdintclean')
else: 
       check2 = True
       print('[INFO] Emission mean <3 sigma different between tclean and sdintclean')

if check1 & check2: 
       print('[WARNING] Checks passed!')
else:
       print('[INFO] One or more checks failed!')