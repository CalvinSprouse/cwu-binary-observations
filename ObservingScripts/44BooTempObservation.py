# this script runs automated observations of multiple targets, filters, and exposures

# imports
from __future__ import print_function

import time

# import astropy
# import astropy.coordinates as coord

from TemplateScripts.Initializer import *

from astropy.coordinates import SkyCoord

# get connection objects
conn, telescope, camera, filterwheel, focuser = connect()

# run a 2 hour observation (at which point refocus)
im_timeout = 2*60*60
start_time = time.time()
im_count = 0
while time.time() - start_time < im_timeout:
    for filter, config in filter_focus_dict:
        focus = config[0]
        exptime = config[1]
        print("Imaging in {0} focusing to {1} for {2} seconds".format(filter, focus, exptime))

        # swap filter
        filterwheel.go_to(filter)
        focuser.go(focus)

        # take picture
        camera.expose(exptime)
        camera.template = "44Boo_PY_{{seq:3}}.fits"

        # short pause
        print("Image complete in {0} @ {1} for {2} seconds".format(filter, focus, exptime))
        time.sleep(1)

    # pause between volleys
    im_count += 1
    print("Volley {0} complete".format(im_count))
    time.sleep(10)