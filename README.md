# sdintimaging
 
This project creates combined images from interferometric and single-dish data.

Test data here: https://www.dropbox.com/scl/fo/eatg6fskssf1du1ovilaq/h?rlkey=f1j4h34vyecvvkrkisw1xlh1b&dl=0 

## Summary

If including data from the e.g. IRAM-30m, first run `update_headers.ipynb` to get the data into the correct format. If you're only interested in combining with TP from ALMA, then this shouldn't be a problem and you don't need to run this step. The main issues this solves in the IRAM data are the following:
 - changes the RA and Dec to -TAN projection
    - without this raises issue using 'importfits'
```
tbd
```
 - updating 'TELESCOP' and 'INSTRUME' in the header to 'ALMA' as IRAM-30m isn't supported in CASA
    - without this raises the following issue using 'imregrid' (which is needed to do spectral regridding before `sdintimaging`)     
```
imregrid::ImageRegrid::regrid (file /source/casa6/casatools/casacore/casacore/images/Images/ImageRegrid.tcc, line 89)Cannot find the observatory name UNKNOWN in the CASA
```
      
## `cloudA_updateheader.py`

The script processes a FITS file containing astronomical data of a spectral cube. Initially, it loads the data and extracts the necessary header information. The data, which is initially in units of Kelvin (K), is then converted to Jansky per beam (Jy/beam) using the given beam dimensions and rest frequency from the header. The code subsequently modifies certain header parameters, like the projection types for spatial axes, and sets placeholders for the telescope and instrument names. With the help of the `spectral_cube` library, the spectral axis of the cube is altered, converting its units from frequency to velocity and then back to frequency. Finally, the modified data, along with its updated header, is saved to a new FITS file, potentially overwriting any existing file with the same name.

## `cloudA_tclean.py`

1. **Handy functions**: A function `add_restoringbeamtable` is defined. It modifies the restoring beam information of a CASA image cube.

    `add_restoringbeamtable`:
    - This function is designed to work with CASA images, especially image cubes. Image cubes in radio astronomy often represent 3D data, with two spatial dimensions (like right ascension and declination) and one frequency or velocity dimension.
    - It retrieves the shape and information of an image and loops through all its channels and polarizations.
    - For each channel and polarization, it sets a restoring beam. The restoring beam is crucial in radio interferometry; it represents the resolution of the observation, akin to the "blurring" you'd get from a telescope's finite size.
      
2. **Configuration settings**:
    - Flags for different processes (`do_clean`, `do_sdprep`, `do_iramprep`, `do_feather`, `do_sdintimaging`, `do_sdintimaging_iram`) are set.
    - Paths for various data files (`filename_12m7mtp`, `filename_12m7m`, etc.) in the directory `'data/cloudA'` are defined.
    - Imaging parameters (like `cell`, `imsize`, `restoringbeam`, etc.) are provided.

3. **Cleaning process (`do_clean`)**:
    - Observational data list (`listobs`) is created.
    - Any existing `_tclean` files in the input directory are removed.
    - The `tclean` function is called to deconvolve and image the visibility data.

4. **Single-dish preparation (`do_sdprep`)**:
    - Existing regrid files related to `filename_tp` are removed.
    - The image is imported from a FITS file, regridded to match the reference `tclean` image, and transposed.
    - A restoring beam table is added to the transposed image.

5. **IRAM preparation (`do_iramprep`)**:
    - Similar to `do_sdprep`, but for `filename_iram`.

6. **Feathering process (`do_feather`)**:
    - Combines the high-resolution `tclean` image with the regridded low-resolution single-dish or IRAM image using the feathering technique.

7. **Single-Dish Interferometric Imaging (`do_sdintimaging` and `do_sdintimaging_iram`)**:
    - The interferometric data (`vis`) is combined with single-dish data (either `filename_tp` or `filename_iram`) using the `sdintimaging` function.
    - The combined image is processed with parameters like `cell`, `imsize`, `nchan`, etc.

The script seems to be modular, meaning specific processes (cleaning, preparation, feathering, etc.) can be turned on or off using the boolean flags at the beginning.
