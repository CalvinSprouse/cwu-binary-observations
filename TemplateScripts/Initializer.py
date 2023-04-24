# this script creates connection objects from the ACE interface
# it really serves no purpose to run this alone
# Python 2


# imports
from __future__ import print_function

import time

import ace.syscore
import ace.telescope
import ace.camera
import ace.dome
import ace.filterwheel
import ace.focuser


# define a function to create a connection to the ACE interface
def connect():
    conn = ace.syscore.AceConnection("localhost")
    conn.authenticate("root", "password")
    print("AceConnection Authenticated {0}".format(conn))

    # create a connection to parts of the telescope
    telescope = ace.telescope.Telescope(conn, "telescope", "Telescope")
    print("Telescope Connected {0}".format(telescope))

    camera = ace.camera.Camera(conn, "telescope", "FLI Camera")
    print("Camera Connected {0}".format(camera))

    filterwheel = ace.filterwheel.FilterWheel(conn, "telescope", "Filter Wheel")
    print("Filter Wheel Connected {0}".format(filterwheel))

    focuser = ace.focuser.Focuser(conn, "telescope", "Focuser")
    print("Focuser Connected {0}".format(focuser))

    # dome = ace.dome.Dome(conn, "telescope", "Dome")
    # print("Dome Connected {0}".format(dome))
    return conn, telescope, camera, filterwheel, focuser


# define functions to output information on telescope parts
def get_telescope_info(telescope_conn: ace.telescope.Telescope) -> dict:
    return {
        "target": telescope_conn.get_target(),
        "position": telescope_conn.get_position(),
    }

def get_camera_info(camera_conn: ace.camera.Camera) -> dict:
    return {
        "state": camera_conn.state,
        "temperature": camera_conn.temperature,
        "target_temperature": camera_conn.setpoint,
        "readout_mode": camera_conn.readout_mode,
        "can_pause": camera_conn.can_pause,
        "template": camera_conn.template,
    }

def get_filterwheel_info(filterwheel_conn: ace.filterwheel.FilterWheel) -> dict:
    return {
        "state": filterwheel_conn.state,
        "position": filterwheel_conn.position,
        "positions": filterwheel_conn.positions,
        "filter_name": filterwheel_conn.filter_name,
        "target": filterwheel_conn.target,
        "names": filterwheel_conn.get_names(),
    }

def get_dome_info(dome_conn: ace.dome.Dome) -> dict:
    return {
        "state": dome_conn.state,
        "azimuth": dome_conn.azimuth,
        "target_azimuth": dome_conn.cmd_azimuth,
        "target_elevation": dome_conn.cmd_elevation,
        "park_azimuth": dome_conn.park_azimuth,
    }

def get_focuser_info(focuser_conn: ace.focuser.Focuser) -> dict:
    return {
        "state": focuser_conn.state,
        "position": focuser_conn.position,
        "target": focuser_conn.target,
        "minimum": focuser_conn.minimum,
        "maximum": focuser_conn.maximum,
    }
