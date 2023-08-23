#### Handy functions
def add_restoringbeamtable(imagename):
        ia.open(imagename)
        shape = ia.shape()
        restoringbeam = ia.restoringbeam()
        ia.close()
        for i in range(shape[0]):
                ia.open(imagename)
                ia.setrestoringbeam(beam=restoringbeam, channel = i, polarization = 0, remove=True)
                ia.close()
####

#### 
filename_12m7mtp = 'data/cloudA/cloudA_12m+7m+tp_n2hp10'
filename_12m7m = 'data/cloudA/cloudA_12m+7m_n2hp10'
filename_tp = 'data/cloudA/cloudA_tp_n2hp10'

vis=['%s.ms' %filename_12m7m] 
cell=['0.5arcsec'] 
imsize=[360, 250]
restoringbeam='common'
phasecenter='ICRS 18:26:18.2934 -012.41.27.253'
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
sdimage='%s_regrid.image'%filename_tp
sdpsf=''
sdgain=1.0
dishdia=12.0

do_clean = False
do_sdprep = True
do_feather = False
do_sdintimaging = False
####


if do_clean:

       rmtables([vis[0]+'.listobs'])
       listobs(vis=vis[0],
              listfile=vis[0]+'.listobs')

       filenames_output = ['.model','.sumwt', '.image.pbcor', '.image', '.psf', '.pb', '.weight', '.residual', '.mask']
       rmtables([filename_12m7m+x for x in filenames_output])

       tclean(vis=vis,
              imagename='%s'%filename_12m7m,
              cell=cell, 
              imsize=imsize,
              phasecenter=phasecenter,
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

if do_sdprep: 

       filenames_output = ['.image', '_regrid.image']
       rmtables([filename_tp+x for x in filenames_output])

       importfits(fitsimage='%s.fits'%filename_tp,
              imagename='%s.image'%filename_tp,
              overwrite=True)

       imregrid(imagename='%s.image'%filename_tp,
              template='%s.image'%filename_12m7m,
              asvelocity=False,
              overwrite=True,
              output='%s_regrid.image'%filename_tp)

       add_restoringbeamtable(imagename='%s_regrid.image'%filename_tp)


if do_feather:

       filenames_output = ['.image']
       rmtables([filename_12m7mtp+x for x in filenames_output])

       feather(imagename='%s.image'%filename_12m7mtp,
              highres='%s.image'%filename_12m7m, 
              lowres='%s.image'%filename_tp)

if do_sdintimaging:
       sdintimaging(usedata=usedata,
              sdimage=sdimage,
              sdpsf=sdpsf,
              sdgain=sdgain,
              dishdia=dishdia,
              vis=vis,
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
