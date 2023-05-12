# to be run after a multi target observation to fix fits headers
# because default code wont update the object fits parameter

# python version 3.8+ but may work with 2 if ccdproc has Python 2 version

# imports
import os
import warnings

import ccdproc
from astropy.io import fits
from astropy.utils.exceptions import AstropyWarning

# suppress fits file warnings
warnings.filterwarnings("ignore", category=AstropyWarning, append=True)


def fix_fits_objects():
    # get a list of fits files in directory (run program in same folder as fits files)
    fits_list = ccdproc.ImageFileCollection(os.getcwd(), include_path=False)

    # iterate over fits files to extract parameters from name
    for fits_file in fits_list:
        print("Adjusting {0}.".format(fits_file))

        # fits files will be in the following form (from MultiTargetObservation)
        # [prefix]_[target]_[filter]_[exposure]_[sequence]_PY.fits
        parameters = str(fits_file).split("_").reverse()

        # extract parameters sequentially
        # suffix will be PY.fits and is useuless
        suffix = parameters.pop()
        sequence = parameters.pop()
        exposure = parameters.pop()
        filter = parameters.pop()
        target = parameters.pop()

        # read in fits header
        fits_data = ccdproc.CCDData.read(fits_file)

        # replace object with target
        print("Replaced OBJECT={0} with OBJECT={1}".format(fits_data.meta["OBJECT"], target))
        fits_data.meta["OBJECT"] = target

        # re-write fits file with updated header
        fits_data.write(fits_file, overwrite=True)