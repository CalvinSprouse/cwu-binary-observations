"""
Objective: Image an eclipsing binary in multiple filters

Parameters:
"""

# imports
import astropy
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

import ace.syscore
import ace.camera
import ace.telescope
import ace.filterwheel
import ace.focuser
import ace.dome

import logging
import sys
import time


# configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s : [%(levelname)s] : %(message)s",
    handlers=[
        logging.FileHandler("observation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


# define parameters
# in seconds
astropy.utils.data.Conf.remote_timeout = 60
logging.debug("Timeout:{0}".format(astropy.utils.data.Conf.remote_timeout))

# cycle lists desired parameters to use for each observation loop
filter_cycle = ("Bessel V", "Bessel B")
exposure_cycle = (20, 10)

# target (name in stellarium for astropy lookup)
observation_target = "44 Boo"
target_pos = SkyCoord.from_name(target_name)
logging.debug("Initial Position:{0}/{1}".format(target_pos.ra, target_pos.dec))

# file name format lambda function
file_name = lambda target, filter, exposure, count : "{0}_{1}_{2}_{3}.fits".format(target, filter, exposure, count)

# number of hours to run the observation loop
observation_time = 6

# wait interval [seconds]
image_pause = 60


# connect to telescope
# create a connection client
conn = ace.syscore.AceConnection("localhost")
conn.authenticate("root", "password")
logging.debug("Connector authenticated")

# create a camera
camera = ace.camera.Camera(conn, "telescope", "FLI Camera")
logging.debug("Camera created")

# create a telescope
telescope = ace.telescope.Telescope(conn, "telescope", "Telescope")
logging.debug("Telescope created")

# create a dome
dome = ace.dome.Dome(conn, "telescope", "Dome")
logging.debug("Dome created")

# create a filterwheel
filterwheel = ace.filterwheel.FilterWheel(conn, "telescope", "FilterWheel")
logging.debug("FilterWheel1 created")

filterwheel2 = ace.filterwheel.FilterWheel(conn, "telescope", "FilterWheel2")
logging.debug("FilterWheel2 created")

# create a focuser
focuser = ace.focuser.Focuser(conn, "telescope", "Focuser")
logging.debug("Focuser created")

logging.info("Computer Initialized")


# code exposure loop
# check for ccd temp stability
start_ccd_temp = camera.temperature
logging.debug("Start Temp {0}".format(start_ccd_temp))

# setup observation timer
start_time = time.time()
elapsed_hours = lambda : (time.time()-start_time)/3600
logging.debug("Started @ {0}".format(start_time))

# image counter
image_count = 0

while True:
    # check telescope position
    telescope.go_to_j2000(target_pos.ra.degree, target_pos.dec.degree)
    logging.info("Moving Telescope {0}".format(telescope.get_target()))

    # log temperature
    logging.debug("CCD Temp {0}".format(camera.temperature))

    # start imaging
    for filter in filter_cycle:
        for exposure in exposure_cycle:
            logging.info("Imaging with filter:{0} exposure:{1}".format(filter, exposure))
            template = file_name(target, filter, exposure, image_count)
            # TODO: MAKE FILTER FUNCTION
            # set_filter(filter)
            # log it
            camera.template = template
            camera.expose(exposure)
            logging.info("Saving image to {0}".format(template))

    # check end condition before sleep
    if elapsed_hours <= observing_time:
        logging.info("Observation time ended")
        break

    # wait
    logging.info("Pausing {0}s".format(pause))
    time.sleep(image_pause)

    # iterate
    image_count += 1

# end observation
logging.info("Observations Complete")
camera = None
telescope = None
dome = None
filterwheel1 = None
filterwheel2 = None
focuser = None
