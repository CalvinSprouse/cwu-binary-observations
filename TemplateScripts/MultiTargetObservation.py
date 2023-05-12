# Python Version: 2

### imports
# this import is for the better print function
from __future__ import print_function

# module imports
import time
from datetime import datetime

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.coordinates.name_resolve import NameResolveError
from astropy.utils import iers

# reallly really bad practice but just stop with the warnings
import warnings
warnings.filterwarnings("ignore")

# import ace.syscore
# import ace.telescope
# import ace.camera
# import ace.dome
# import ace.filterwheel
# import ace.focuser

# imports from local .py files
from Initializer import *
from ObsConfig import *
# from FitsObjFixer import fix_fits_objects


### set astropy connection tables (for some reason)
# iers_a = iers.IERS_A.open("http://datacenter.iers.org/data/9/finals2000A.all")
# iers.IERS_A.iers_table = iers_a


### get telescope connection objects
conn, telescope, camera, filterwheel, focuser = connect()


### establish location/time (will update periodically)
current_location = EarthLocation.from_geodetic(lat=47.00*u.deg, lon=-120.54*u.deg, height=400*u.m)
current_time = Time(datetime.utcnow(), location=current_location)
print("Established current location (do not attempt to read) {0} and current time {1}.".format(current_location, current_time))

# get the lst
# print("Established current LST {0}.")


### define a function to reset the telescope between images
def reset_for_imaging(observation, safety_seconds=5):
    # get current time for coordinate transformation
    current_time = Time(datetime.utcnow(), location=current_location)

    # get the az/alt of the target
    radec = SkyCoord(ra=observation["target_pos"][0]*u.deg, dec=observation["target_pos"][1]*u.deg)
    azalt = radec.transform_to(AltAz(obstime=current_time, location=current_location))
    az = azalt.az.deg
    alt = azalt.alt.deg
    print("Checked az {0} alt {1}.".format(az, alt))

    # check that coordinates do not take the telescope to an illegal position
    # if 90 < az < 180 and alt < 20 (illegal)
    # if 180 < az < 360 and alt < 40 (illegal)
    # add 5 degress for safety
    # these values could defo be tweaked
    if (0 < az and az < 180) and (alt >= 25): pass
    elif (180 <= az and az <= 360) and (alt >= 45): pass
    else:
        # object is too low in its part of the sky, this is a harsh method but its safe
        print("{0} too low, skipping. (Az:{1}, Alt:{2})".format(observation["target_name"], az, alt))

        # false return causes skipped object
        return False

    # move telescope
    telescope.go_to_j2000(observation["target_pos"][0], observation["target_pos"][1])

    # "wait until" telescope in position
    while (abs(telescope.get_target().ra - telescope.get_position()[0]) > 0.5) and (abs(telescope.get_target().dec - telescope.get_position()[1]) < 0.5):
       # print("> Slewing to {0} from {1}".format(telescope.get_target().ra, telescope.get_position()))
       time.sleep(safety_seconds)

    # reset filter to fix wheel positions
    # print("> Moving Filter Wheel")
    filterwheel.go_to("Empty")

    # "wait until" filterwheel in position
    while filterwheel.state == ace.filterwheel.state.MOVING: time.sleep(safety_seconds)

    # change filter to actual filter required for observation
    filterwheel.go_to(observation.get("filter_name"))

    # "wait until" filterwheel in position
    while filterwheel.state == ace.filterwheel.state.MOVING: time.sleep(safety_seconds)

    # print("> Focusing")
    # change focus
    focuser.go(filter_focus_dict[observation.get("filter_name")])

    # "wait until" focuser in position
    while focuser.state != ace.focuser.state.STOPPED: time.sleep(safety_seconds)

    # configure camera
    camera.template = "{0}_{1}_{2}_{3}_".format(
        observation.get("file_prefix").replace(" ", "-"),
        observation.get("target_name").replace(" ", "-"),
        observation.get("filter_name").replace(" ", "-"),
        str(observation.get("exp_time")).replace(".", "-"),) + "{{seq:3}}_PY.fits"
    time.sleep(safety_seconds)

    # true return means good to take pictures!
    return True


### define a function to run a single observation loop
def do_observations():
    for observation in obs_list:
        # move the telescope to the observation target
        print("\nResetting telescope for new observation of {0}.".format(observation["target_name"]))

        # attempt to reset the telescope but skip the target if false return
	if not reset_for_imaging(observation): continue

        # get information for readout
        telescope_info = get_telescope_info(telescope)
        camera_info = get_camera_info(camera)
        filterwheel_info = get_filterwheel_info(filterwheel)
        focuser_info = get_focuser_info(focuser)

        # give readout
        print("Telescope configured for observing {0}.".format(observation["target_name"]))
        print("Moved telescope to {0}.".format(telescope_info["position"]))
        print("Set camera template to {0}.".format(camera_info["template"]))
        print("Set filter to {0}.".format(filterwheel_info["filter_name"]))
        print("Set focuser to {0}.".format(focuser_info["position"]))

        # get the lst, this helps generate a "safe position" in case of going too low into the horizon
        # current_lst = Time(datetime.utcnow(), location=current_location).sidereal_time("mean").deg

        # take the image
        for img_index in range(observation["img_count"]):
            # TODO: Integrate binning/cropping
            exp_time = observation.get("exp_time")
            print("Exposing for {0}. ({1}/{2})".format(exp_time, img_index+1, observation.get("img_count")))
            camera.expose(exp_time)

            # "wait until"
            while camera.state == ace.camera.state.EXPOSING: time.sleep(1)
            print("Exposure complete.")

        # check for time end condition end conditions
        if time.time() - start_time > obs_time*60*60:
            print("Reached maximum observation time of {0} hours.".format(obs_time))
            # return False to stop looping
            return False

        # check for pause between observations
        if observation.get("pause_time") > 0:
            print("Pausing for {0} seconds.".format(observation.get("pause_time")))
            time.sleep(observation.get("pause_time"))

    # return True to continue looping
    return True


### parse through the observation list (pre-error checking)
obs_list_ok = True
for index in range(len(obs_list)):
    # get the observation for easy access
    observation = obs_list[index]

    # create an error string to print in front of all errors
    error_str_prefix = "Error in observation {0}:".format(index)

    # check for a target_pos overwrite
    # if there is none then try to find the position from astropy
    # and do error checking on the name
    try:
        if observation.get("target_name"):
            try:
                position = SkyCoord.from_name(observation.get("target_name"))
            except NameResolveError:
                print(error_str_prefix + "Error when trying to get the position of {}. Fix in obs_list and try again.".format(observation.get("target_name")))
                obs_list_ok = False
        # if the object appears to exist then record its position in the target_pos slot
        obs_list[index]["target_pos"] = (position.ra.degree, position.dec.degree)
    except KeyError:
        print(error_str_prefix + "Required entry target_name not found.")
        obs_list_ok = False

    # check that the filter name is in the filter
    # focus wheel dict
    try:
        if not observation.get("filter_name") in filter_focus_dict:
            print(error_str_prefix + "Filter {0} not found in the filter to focus dict.".format(observation.get("filter_name")))
            obs_list_ok = False
    except KeyError:
        print(error_str_prefix + "Required entry filter_name not found.")
        obs_list_ok = False

    # check that the exposure time is a positive number
    try:
        if observation.get("exp_time") <= 0:
            print(error_str_prefix + "exp_time {0} appears to be negative.".format(observation.get("exp_time")))
            obs_list_ok = False
    except KeyError:
        print(error_str_prefix + "Required entry exp_time not found.")
        obs_list_ok = False

    # check that img count is not negative
    # if it does not exist supply default value
    try:
        if observation.get("img_count") <= 0:
            print(error_str_prefix + "img_count {0} appears to be negative.".format(observation.get("img_count")))
            obs_list_ok = False
    except KeyError:
        obs_list[index]["img_count"] = 1

    # check that pause time is not negative
    # if it does not exist supply default value
    try:
        if observation.get("pause_time") <= 0:
            print(error_str_prefix + "pause_time {0} appears to be negative.".format(observation.get("pause_time")))
            obs_list_ok = False
    except KeyError:
        obs_list[index]["pause_time"] = 1

    # supply default file prefix if it does not exist
    if not observation.get("file_prefix", None):
        obs_list[index]["file_prefix"] = ""


# if any errors occured stop program execution and warn user
if obs_list_ok:
    ### begin observation loop
    start_time = time.time()
    obs_loops = 0
    while True:
        # iterate obs_loops
        obs_loops += 1

        # do an observation loop and check for end conditions
        if not do_observations(): break
        elif obs_loops >= obs_loop and obs_loop > 0:
            print("Reached maximum loops of {0}.".format(obs_loop))
            break
        time.sleep(obs_pause)

    ### close telescope connections
    print("Imaging complete.")
else:
    print("Errors were found during obs_list check. Fix and re-run.")

### disconnect
conn = None
telescope = None
camera = None
filterwheel = None
focuser = None
