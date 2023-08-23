def add_restoringbeamtable(imagename):

        ia.open(imagename)
        shape = ia.shape()
        restoringbeam = ia.restoringbeam()
        ia.close()

        for i in range(shape[0]):
                ia.open(imagename)
                ia.setrestoringbeam(beam=restoringbeam, channel = i, polarization = 0, remove=True)
                ia.close()