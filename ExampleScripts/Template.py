"""
Objective:

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

# file name
file_name = lambda target, filter, exposure, count : "{0}_{1}_{2}_{3}.fits".format(target, filter, exposure, count)

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


# end observation
logging.info("Observations Complete")
camera = None
telescope = None
dome = None
filterwheel1 = None
filterwheel2 = None
focuser = None
