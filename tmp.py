def add_restoringbeamtable(inputfile):

        ia.open(inputfile)
        shape = ia.shape()
        restoringbeam = ia.restoringbeam()
        ia.close()

        for i in range(shape[0]):
                ia.open(inputfile)
                ia.setrestoringbeam(beam=restoringbeam, channel = i, polarization = 0, remove=True)
                ia.close()