# Python Version: 2

### imports
# this import is for the better print function
from __future__ import print_function

# module imports
import time
from datetime import datetime

import astropy.units as u

# really bad practice but i was so fed up with the warnings
import warnings
warnings.filterwarnings("ignore")

# import from the local initializer
from Initializer import *
from ObsConfig import *


### define how many of each dark to take
# this number should be odd and at least 3
dark_exp_count = 5


### get telescope connection objects
conn, telescope, camera, filterwheel, focuser = connect()


### get all unique dark times
# the set only includes unique items so duplicate exposures will
# be removed automatically
dark_times = set([d.get("exp_time") for d in obs_list if "exp_time" in d])


### iterate over the list of dark times and take darks!
for dark_time in dark_times:
    # pause between imaging (safety)
    time.sleep(1)
    for img_index in range(dark_exp_count):
        print("Taking {0}/{1} {2} second darks.".format(dark_exp_count, img_index, dark_time))

        # reset the camera template
        camera.template = "Dark_{1}_".format(dark_time) + "{{seq:3}}_PY.fits"

        # expose
        camera.expose(dark_time, type=ace.camera.exposure_type.DARK)

        # wait until done
        while camera.state == ace.camera.state.EXPOSING: time.sleep(1)
