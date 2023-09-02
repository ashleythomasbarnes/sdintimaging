#### 
input_dir = 'data/cloudA'
filename_12m7mtp_tclean = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_tcleanfeather.image'
filename_12m7mtp_sdint = f'{input_dir}/cloudA_12m+7m+tp_n2hp10_sdintimaging.joint.cube.image.pbcor'
####

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

stats_rms = imstat(imagename='%s.rms'%filename_12m7mtp_sdint)

os.system('rm -rf %s/immath_diff.image'%input_dir)
immath(imagename=[filename_12m7mtp_tclean, filename_12m7mtp_sdint],
		outfile='%s/immath_diff.image'%input_dir,
		expr='IM0-IM1')

stats_diff = imstat(imagename='%s/immath_diff.image'%input_dir)
