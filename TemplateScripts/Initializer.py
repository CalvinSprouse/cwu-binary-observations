# this script creates connection objects from the ACE interface
# it really serves no purpose to run this alone
# Python Version: 2

# imports
from __future__ import print_function

import time

import astropy.units as u
from astropy.coordinates import SkyCoord, AltAz

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

    focuser = ace.focuser.Focuser(conn, "telescope", "Main Focus")
    print("Focuser Connected {0}".format(focuser))

    # dome = ace.dome.Dome(conn, "telescope", "Dome")
    # print("Dome Connected {0}".format(dome))
    return conn, telescope, camera, filterwheel, focuser


# define functions to output information on telescope parts
def get_telescope_info(telescope_conn):
    return {
        "target": telescope_conn.get_target(),
        "position": telescope_conn.get_position(),
    }

def get_camera_info(camera_conn):
    return {
        "state": camera_conn.state,
        "temperature": camera_conn.temperature,
        "target_temperature": camera_conn.setpoint,
        "readout_mode": camera_conn.readout_mode,
        "can_pause": camera_conn.can_pause,
        "template": camera_conn.template,
    }

def get_filterwheel_info(filterwheel_conn):
    return {
        "state": filterwheel_conn.state,
        "position": filterwheel_conn.position,
        "positions": filterwheel_conn.positions,
        "filter_name": filterwheel_conn.filter_name,
        "target": filterwheel_conn.target,
        "names": filterwheel_conn.get_names(),
    }

def get_dome_info(dome_conn):
    return {
        "state": dome_conn.state,
        "azimuth": dome_conn.azimuth,
        "target_azimuth": dome_conn.cmd_azimuth,
        "target_elevation": dome_conn.cmd_elevation,
        "park_azimuth": dome_conn.park_azimuth,
    }

def get_focuser_info(focuser_conn):
    return {
        "state": focuser_conn.state,
        "position": focuser_conn.position,
        "target": focuser_conn.target,
        "minimum": focuser_conn.minimum,
        "maximum": focuser_conn.maximum,
    }


# define functions to move the telescope and components safely
def move_telescope(telescope, ra_deg, dec_deg, current_location, current_time, safety_pause=5):
    # returns true if moved successfully, false otherwise
    # convert ra dec to az alt and check against limits
    radec = SkyCoord(ra=ra_deg*u.deg, dec=dec_deg*u.deg)
    azalt = radec.transform_to(AltAz(obstime=current_time, location=current_location))
    az = azalt.az.deg
    alt = azalt.alt.deg
    print("Found az: {0}, alt: {1}.".format(az, alt))

    # check, if pass then the position is safe
    # if the position is not safe return false
    # the main ctrl script will determine from there what to do
    if (0 < az and az < 180) and (alt >= 25): pass
    elif (180 <= az and az <= 360) and (alt > 45): pass
    else: return False

    # the position was safe so start slewing
    print("Moving telescope to ra: {0}, dec: {1}.".format(ra_deg*24/360, dec_deg*24/260))
    telescope.go_to_j2000(ra_deg, dec_deg)

    # wait for the telescope to finish moving
    target_ra = telescope.get_target().ra
    target_dec = telescope.get_target().dec
    while ((abs(target_ra - telescope.get_position()[0]) > 0.1)
           and (abs(target_dec - telescope.get_position()[0] > 0.1))):
        time.sleep(safety_pause)

    # telescope is stopped so return True
    return True

def change_filter(filterwheel, target_filter, safety_pause=5):
    # returns True if changed successfully, otherwise False
    empty_name = "Empty"

    # start by resetting the filterwheel using recursion
    if target_filter != empty_name:
        change_filter(filterwheel, target_filter=empty_name, safety_pause=safety_pause)

    # move to target position
    print("Moving filterwheel to {0}.".format(target_filter))
    filterwheel.go_to(target_filter)

    # wait until not moving
    while filterwheel.state == ace.filterwheel.state.MOVING: time.sleep(safety_pause)

    # filter changed so return True
    return True

def change_focus(focuser, target_focus, safety_pause=5):
    # returns True if changed successfullty, otherwise False
    print("Moving main focus to {0}.".format(target_focus))
    focuser.go(target_focus)

    # wait for not moving
    while focuser.state != ace.focuser.state.STOPPED: time.sleep(safety_pause)

    # successful move so return True
    return True