
filename = 'data/cloudA/cloudA_12m+7m_n2hp10'

vis=['%s.ms' %filename] 
imagename=r'%s' %filename
cell=['0.5arcsec'] 
imsize = [300,300]
stokes='I' 
specmode='cube' 
outframe='LSRK'
gridder='mosaic' 
usepointing=False 
mosweight=True
pblimit=0.2 
deconvolver='hogbom' 
pbcor=True
weighting='briggs' 
robust=2.0 
niter=600000 
threshold='0.015Jy'
usemask='auto-multithresh' 
sidelobethreshold=2.0
noisethreshold=4.25
lownoisethreshold=1.5 
negativethreshold=0
minbeamfrac=0.3 
growiterations=50 
minpercentchange=1.0 

do_clean = True
if do_clean:
       tclean(vis=vis,
              imagename=imagename,
              cell=cell, 
              imsize=imsize,
              stokes=stokes, 
              specmode=specmode, 
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

do_sdintimaging = False
if do_sdintimaging:
       sdintimaging(vis=vis,
              imagename=imagename,
              cell=cell, 
              imsize=imsize,
              stokes=stokes, 
              specmode=specmode, 
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


