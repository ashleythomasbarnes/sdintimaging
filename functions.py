#### Handy functions
def add_restoringbeamtable(imagename):

       cube_info = imhead(imagename, mode='list')
       n_chan = cube_info['shape'][-1]
       n_pol = cube_info['shape'][-2]

       ia.open(imagename)
       restoring_beam = ia.restoringbeam()
       ia.setrestoringbeam(remove=True)
       for c in range(n_chan):
              for p in range(n_pol):
                     ia.setrestoringbeam(beam=restoring_beam, channel=c, polarization=p)
       ia.close()
       imhead(imagename, 'put', 'CASAMBM', 'T')
####
