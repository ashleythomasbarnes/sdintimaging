from functions import *

#### 
do_clean = True
do_sdprep = False
do_iramprep = False
do_feather = False
do_sdintimaging = False
do_sdintimaging_iram = False

input_dir = 'data/cloudA'
filename_12m7mtp = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_single'
filename_12m7m = f'{input_dir}/cloudA_12m+7m_n2hp10_single'
filename_tp = f'{input_dir}/cloudA_tp_n2hp10'
filename_iram =  f'{input_dir}/cloudA_iram_n2hp10'
filename_12m7miram = f'{input_dir}/cloudA_12m+7m+iram_n2hp10'

vis=['%s.ms' %filename_12m7m] 
cell=['0.5arcsec'] 
imsize=[360, 250]
restoringbeam='common'
phasecenter='ICRS 18:26:18.2934 -012.41.27.253'
stokes='I' 
specmode='cube' 
outframe='LSRK'
nchan=1
start=1
width=1
gridder='mosaic' 
usepointing=False 
mosweight=True
pblimit=0.2 
deconvolver='hogbom' 
pbcor=True
weighting='briggs' 
robust=2.0 
niter=600000 
threshold='0.03Jy'
usemask='auto-multithresh' 
sidelobethreshold=2.0
noisethreshold=4.25
lownoisethreshold=1.5 
negativethreshold=0
minbeamfrac=0.3 
growiterations=50 
minpercentchange=1.0 

usedata='sdint'
sdpsf=''
sdgain=1.0
####


##################
if do_clean:

       listobs(vis=vis[0],
              listfile=vis[0]+'.listobs',
              overwrite=True)

       os.system('rm -rf %s_tclean*'%filename_12m7m)

       tclean(vis=vis,
              imagename='%s_tclean'%filename_12m7m,
              cell=cell, 
              imsize=imsize,
              restoringbeam=restoringbeam, #commonbeam, feather will not work without
              phasecenter=phasecenter,
              stokes=stokes, 
              specmode=specmode,
              nchan=nchan,
              start=start,
              width=width,
              outframe=outframe,
              gridder=gridder, 
              pblimit=pblimit, 
              deconvolver=deconvolver, 
              pbcor=pbcor,
              weighting=weighting, 
              robust=robust, 
              niter=niter, 
              threshold=threshold,
              usemask=usemask, 
              sidelobethreshold=sidelobethreshold,
              noisethreshold=noisethreshold,
              lownoisethreshold=lownoisethreshold, 
              negativethreshold=negativethreshold,
              minbeamfrac=minbeamfrac, 
              growiterations=growiterations, 
              minpercentchange=minpercentchange)

       exportfits(imagename='%s_tclean.image.pbcor'%filename_12m7m,
              fitsimage='%s_tclean.image.pbcor.fits'%filename_12m7m,
              velocity=True,
              overwrite=True)


##################
if do_sdprep: 

       os.system(f'rm -rf {filename_tp}_regrid*')

       importfits(fitsimage='%s.fits'%filename_tp,
              imagename='%s.image'%filename_tp,
              overwrite=True)

       imregrid(imagename='%s.image'%filename_tp,
              template='%s_tclean.image'%filename_12m7m,
              asvelocity=False,
              overwrite=True,
              output='%s_regrid.image'%filename_tp)

       imtrans(imagename='%s_regrid.image'%filename_tp,
              outfile='%s_regrid_trans.image'%filename_tp,
              order=['rig', 'declin', 'stok', 'frequ'])

       os.system('cp -r %s_regrid_trans.image %s_regrid_trans_beams.image' %(filename_tp, filename_tp))
       add_restoringbeamtable(imagename='%s_regrid_trans_beams.image'%filename_tp)


##################
if do_iramprep: 

       os.system(f'rm -rf {filename_iram}_regrid*')

       importfits(fitsimage='%s.fits'%filename_iram,
              imagename='%s.image'%filename_iram,
              overwrite=True,
              defaultaxes=True,
              defaultaxesvalues=['','','','I'])

       imregrid(imagename='%s.image'%filename_iram,
              template='%s_tclean.image'%filename_12m7m,
              asvelocity=False,
              overwrite=True,
              output='%s_regrid.image'%filename_iram)

       imtrans(imagename='%s_regrid.image'%filename_iram,
              outfile='%s_regrid_trans.image'%filename_iram,
              order=['rig', 'declin', 'stok', 'frequ'])

       os.system('cp -r %s_regrid_trans.image %s_regrid_trans_beams.image' %(filename_iram, filename_iram))
       add_restoringbeamtable(imagename='%s_regrid_trans_beams.image'%filename_iram)


##################
if do_feather:

       os.system(f'rm -rf {input_dir}/*_tcleanfeather*')

       feather(imagename='%s_tcleanfeather.image'%filename_12m7mtp,
              highres='%s_tclean.image.pbcor'%filename_12m7m, 
              lowres='%s_regrid_trans.image'%filename_tp)

       feather(imagename='%s_tcleanfeather.image'%filename_12m7miram,
              highres='%s_tclean.image.pbcor'%filename_12m7m, 
              lowres='%s_regrid_trans.image'%filename_iram)

       exportfits(imagename='%s_tcleanfeather.image'%filename_12m7mtp,
              fitsimage='%s_tcleanfeather.image.fits'%filename_12m7mtp,
              velocity=True,
              overwrite=True)

       exportfits(imagename='%s_tcleanfeather.image'%filename_12m7miram,
              fitsimage='%s_tcleanfeather.image.fits'%filename_12m7miram,
              velocity=True,
              overwrite=True)

##################
if do_sdintimaging:

       dishdia=12.0

       os.system('rm -rf %s_sdintimaging*' %filename_12m7mtp)

       sdimage='%s_regrid_trans.image'%filename_tp
       sdintimaging(usedata=usedata,
              sdimage=sdimage,
              sdpsf=sdpsf,
              sdgain=sdgain,
              dishdia=dishdia,
              vis=vis,
              imagename='%s_sdintimaging'%filename_12m7mtp,
              cell=cell, 
              imsize=imsize,
              phasecenter=phasecenter,
              stokes=stokes, 
              specmode=specmode,
              nchan=nchan,
              start=start,
              width=width, 
              outframe=outframe,
              gridder=gridder, 
              pblimit=pblimit, 
              deconvolver=deconvolver, 
              pbcor=pbcor,
              weighting=weighting, 
              robust=robust, 
              niter=niter, 
              threshold=threshold,
              usemask=usemask, 
              sidelobethreshold=sidelobethreshold,
              noisethreshold=noisethreshold,
              lownoisethreshold=lownoisethreshold, 
              negativethreshold=negativethreshold,
              minbeamfrac=minbeamfrac, 
              growiterations=growiterations, 
              minpercentchange=minpercentchange)

       exportfits(imagename='%s_sdintimaging.joint.cube.image.pbcor'%filename_12m7mtp,
              fitsimage='%s_sdintimaging.joint.cube.image.pbcor.fits'%filename_12m7mtp,
              velocity=True,
              overwrite=True)

       sdimage='%s_regrid_trans_beams.image'%filename_tp
       sdintimaging(usedata=usedata,
              sdimage=sdimage,
              sdpsf=sdpsf,
              sdgain=sdgain,
              dishdia=dishdia,
              vis=vis,
              imagename='%s_sdintimaging_beams'%filename_12m7mtp,
              cell=cell, 
              imsize=imsize,
              phasecenter=phasecenter,
              stokes=stokes, 
              specmode=specmode,
              nchan=nchan,
              start=start,
              width=width, 
              outframe=outframe,
              gridder=gridder, 
              pblimit=pblimit, 
              deconvolver=deconvolver, 
              pbcor=pbcor,
              weighting=weighting, 
              robust=robust, 
              niter=niter, 
              threshold=threshold,
              usemask=usemask, 
              sidelobethreshold=sidelobethreshold,
              noisethreshold=noisethreshold,
              lownoisethreshold=lownoisethreshold, 
              negativethreshold=negativethreshold,
              minbeamfrac=minbeamfrac, 
              growiterations=growiterations, 
              minpercentchange=minpercentchange)

       exportfits(imagename='%s_sdintimaging_beams.joint.cube.image.pbcor'%filename_12m7mtp,
              fitsimage='%s_sdintimaging_beams.joint.cube.image.pbcor.fits'%filename_12m7mtp,
              velocity=True,
              overwrite=True)

##################
if do_sdintimaging_iram:
       
       dishdia=30.0

       os.system('rm -rf %s_sdintimaging*' %filename_12m7miram)

       sdimage='%s_regrid_trans.image'%filename_iram
       sdintimaging(usedata=usedata,
              sdimage=sdimage,
              sdpsf=sdpsf,
              sdgain=sdgain,
              dishdia=dishdia,
              vis=vis,
              imagename='%s_sdintimaging'%filename_12m7miram,
              cell=cell, 
              imsize=imsize,
              phasecenter=phasecenter,
              stokes=stokes, 
              specmode=specmode,
              nchan=nchan,
              start=start,
              width=width, 
              outframe=outframe,
              gridder=gridder, 
              pblimit=pblimit, 
              deconvolver=deconvolver, 
              pbcor=pbcor,
              weighting=weighting, 
              robust=robust, 
              niter=niter, 
              threshold=threshold,
              usemask=usemask, 
              sidelobethreshold=sidelobethreshold,
              noisethreshold=noisethreshold,
              lownoisethreshold=lownoisethreshold, 
              negativethreshold=negativethreshold,
              minbeamfrac=minbeamfrac, 
              growiterations=growiterations, 
              minpercentchange=minpercentchange)

       exportfits(imagename='%s_sdintimaging.joint.cube.image.pbcor'%filename_12m7miram,
              fitsimage='%s_sdintimaging.joint.cube.image.pbcor.fits'%filename_12m7miram,
              velocity=True,
              overwrite=True)
