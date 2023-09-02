
####
input_dir = 'data/cloudA'
filename_12m7m = f'{input_dir}/cloudA_12m+7m_n2hp10'
filename_12m7m_single = f'{input_dir}/cloudA_12m+7m_n2hp10_single'

vis = '%s.ms' %filename_12m7m
outputvis = '%s.ms' %filename_12m7m_single

datacolumn='data'
regridms=True
mode='channel'
nchan=1
start=49
width=1
####

##################
os.system(f'rm -rf {outputvis}')
mstransform(vis=vis,
            outputvis=outputvis,
            datacolumn=datacolumn,
            regridms=regridms,
            mode=mode,
            nchan=nchan,
            start=start,
            width=width)
##################