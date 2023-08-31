# Import necessary libraries/modules
from astropy.io import fits
import numpy as np
from astropy import units as u
from spectral_cube import SpectralCube

inputfile = './data/cloudA/cloudA_iram_n2hp10_old.fits'
outputfile = './data/cloudA/cloudA_iram_n2hp10.fits'
freq_new = 9.317340200000E+10 * u.Hz  # Define the new reference frequency



# Load the FITS file containing the cube data
hdu = fits.open(inputfile)[0] # Open the FITS file and get the first HDU (Header/Data Unit)
header = hdu.header  # Extract the header from the HDU
data = hdu.data  # Extract the data (cube) from the HDU

# Convert the data from Kelvin to Jansky per beam
bmaj = header['BMAJ'] * u.deg  # Major axis of the beam in degrees
bmin = header['BMIN'] * u.deg  # Minor axis of the beam in degrees

# Conversion factor from FWHM to sigma for Gaussian beams
fwhm_to_sigma = 1. / (8 * np.log(2))**0.5

# Calculate the area of the beam
beam_area = 2. * np.pi * (bmaj * bmin * fwhm_to_sigma**2)

# Extract rest frequency from the header and convert to Hz
freq = header['RESTFREQ'] * u.Hz

# Define the equivalency for converting brightness temperature to flux density
equiv = u.brightness_temperature(freq)

# Convert the data from Kelvin to Jansky per beam area
data = data * (u.K).to(u.Jy / beam_area, equivalencies=equiv)
header['BUNIT'] = 'Jy/beam'  # Update the unit in the header

# Create a new HDU with the modified data and header
hdu_new = fits.PrimaryHDU(data, header)

# Remove any PV (Projection Value) cards from the header as they are not needed
del hdu_new.header['PV*']

# Update header with new projection types for the spatial axes
hdu_new.header['CTYPE1'] = 'RA---TAN'  # Right Ascension with tangent projection
hdu_new.header['CTYPE2'] = 'DEC--TAN'  # Declination with tangent projection

# Set placeholders for telescope and instrument (assuming ALMA for this example)
hdu_new.header['TELESCOP'] = 'ALMA'
hdu_new.header['INSTRUME'] = 'ALMA'

# Update the spectral axis using the spectral_cube library
cube = SpectralCube.read(hdu_new)
cube = cube.with_spectral_unit(u.km / u.s, velocity_convention='radio', rest_value=freq_new)  # Convert to velocity
cube = cube.with_spectral_unit(u.Hz)  # Convert back to frequency in Hz

hdu_new = cube.hdu.copy()  # Extract the modified HDU from the cube
hdu_new.header['BUNIT'] = 'Jy/beam'  # Ensure the unit in the header is set correctly

# Save the modified data and header to a new FITS file, overwriting if it already exists
hdu_new.writeto(outputfile, overwrite=True)