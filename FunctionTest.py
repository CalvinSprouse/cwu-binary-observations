# imports
import astropy
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

import ace.syscore
import ace.telescope
import ace.camera
import ace.dome
import ace.filterwheel
import ace.focuser

from __future__ import print_function


### primary assignment function to detect telescope pieces
def computer_configuration(remote_timeout: int = 60):
    """
    Configure the computer, camera, telescope, dome, filterwheel, focuser
    remote_timeout: int, seconds before the program should end if no resposnes
    return: camera, telescope, dome, filterwheel, focuser
    """
    # telescope is the name of the computer, Telescope is the telescope

    # in seconds
    astropy.utils.data.Conf.remote_timeout = 60
    print("> Timeout:{0}".format(astropy.utils.data.Conf.remote_timeout))

    # create a connection client
    conn = ace.syscore.AceConnection("localhost")
    conn.authenticate("root", "password")
    print("> Connector authenticated")

    # create a camera
    camera = ace.camera.Camera(conn, "telescope", "FLI Camera")
    print("> Camera created")

    # create a telescope
    telescope = ace.telescope.Telescope(conn, "telescope", "Telescope")
    print("> Telescope created")

    # create a dome
    dome = ace.dome.Dome(conn, "telescope", "Dome")
    print("> Dome created")

    # create a filterwheel
    filterwheel = ace.filterwheel.FilterWheel(conn, "telescope", "FilterWheel")
    print("> FilterWheel created")

    # create a focuser
    focuser = ace.focuser.Focuser(conn, "telescope", "Focuser")
    print("> Focuser created")

    return camera, telescope, dome, filterwheel, focuser


### test call functions
def telescope_test_calls(tele_conn: ace.telescope.Telescope):
    """ Should print a bunch of telescope information """
    print("> Telescope Test Calls")
    print("get_target():{0}".format(tele_conn.get_target()))
    print("get_position():{1}".format(tele_conn.get_position()))


def camera_test_calls(cam_conn: ace.camera.Camera):
    """ prints a bunch of camera info """
    print("> Camera Test Calls")
    print("state:{0}".format(cam_conn.state))
    print("temperature:{0}".format(cam_conn.temperature))
    print("[ccd target temp];setpoint:{0}".format(cam_conn.setpoint))
    print("readout_mode:{0}".format(cam_conn.readout_mode))
    print("can_pause:{0}".format(cam_conn.can_pause))


def dome_test_calls(dome_conn: ace.dome.Dome):
    """ Should print a bunch of dome info """
    print("> Dome test calls")
    print("azimuth:{0}".format(dome_conn.azimuth))
    print("cmd_azimuth:{0}".format(dome_conn.azimuth))
    print("cmd_elevation:{0}".format(dome_conn.cmd_elevation))
    print("park_azimuth:{0}".format(dome_conn.park_azimuth))
    print("state:{0}".format(state))


def filterwheel_test_calls(filter_conn: ace.filterwheel.FilterWheel):
    """ Should print a bunch of filter wheel info """
    print("> FilterWheel test calls")
    print("state:{0}".format(filter_conn.state))
    print("position:{0}".format(filter_conn.position))
    print("positions:{0}".format(filter_conn.positions))
    print("filter_name:{0}".format(filter_conn.filter_name))
    print("target:{0}".format(filter_conn.target))
    print("get_names():{0}".format(filter_conn.get_names()))
    print("get_focus_offset():{0}".format(filter_conn.get_focus_offset()))
    print("get_focus_offsets():{0}".format(filter_conn.get_focus_offsets()))


def focuser_test_calls(focuser_conn: ace.focuser.Focuser):
    """ Should print a bunch of focuser info """
    print("> Focuser test calls")
    print("state:{0}".format(focuser_conn.state))
    print("position:{0}".format(focuser_conn.position))
    print("target:{0}".format(focuser_conn.target))
    print("minimum:{0}".format(focuser_conn.minimum))
    print("maximum:{0}".format(focuser_conn.maximum))
    # note you can make presets for focuser positions (seperate from filterwheel offsets??)
    print("list_presets():{0}".format(focuser_conn.list_presets()))


# get connection objects
camera, telescope, dome, filterwheel, focuser = computer_configuration()

# run test calls
telescope_test_calls(telescope)
camera_test_calls(camera)
dome_test_calls(dome)
filterwheel_test_calls(filterwheel)
focuser_test_calls(focuser)

""" CAMERA
based on a list of exposure times/filters
the camera can be configured to take specific calibration images

ex:
exp_list = (('R', 30s), ('B', 20s))

# reset the file name template
camera.template = DARK_{{seq:3}}.fits

# takes dark exposures
camera.expose(exptime=30, type=ace.camera.DARK)
camera.expose(exptime=20, type=ace.camera.DARK)
# this is for the flats
camera.expose(exptime=2, type=ace.camera.DARK)

# reset the template
camera.template = BIAS_{{seq:3}}.fits

# takes biases
# make a loop for x images
camera.expose(type=ace.camera.BIAS)

in practice this is not that useful since calibration
is finicky and should be done manually but it is possible

note however that a function could/should? be made
for wrapping camera.expose to ensure ccd temp is correct
"""

""" TELESCOPE
the telescope only has go to commands and get target commands
fairly simple and nothing to elaborate on
"""

""" DOME
moving the dome is pretty much never useful as the dome should
be linked to the telescope

we can tell the dome to open and close manually
but that is a bad idea

the dome has several getters that could be referenced
"""

""" FILTERWHEEL
the filterwheel identifies positions by name or number (init = 0)
it is unclear if the filter wheel resets 0 every time it is init
if so then position is relative
we can review this by calling positions
we can also get the name of the filter by calling filter_name
we can get a list of names from get_names()
we can also set names by calling set_names() with a list of strings
each filter can have a focus offset get_focus_offset()
we can also set focus offsets by calling set_focus_offsets() with a float list

the workflow may look like this

run startup
run flats/calibration images
run focus routine for each filter
save values and pass them to code on startup
code identifies filter wheel position and applies offsets
it is unclear how we will differentiate wheel 1 from wheel 2
"""

""" FOCUSER
the focus wheel can be sent to any number of positons
it can also have presets defined
it can also be sent to max/min
it is possible to make a list of presets based on filters
this however feels like bad practice
instead we should identify offsets and save those with the filterwheel
then on every filterwheel change simply call:

focuser.go(filterwheel.get_focus_offset())

with the knowledge that we make each offset just the focus value of the filter

for bet practice this should all be done in a function which changes filters
"""
