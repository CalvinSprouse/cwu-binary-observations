### imports
# this import is for the better print function
from __future__ import print_function

# module imports
import time
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError

# imports from local .py files
from Initializer import *
from ObsConfig import *
from ObsDataFixer import *


### get telescope connection objects
conn, telescope, camera, filterwheel, focuser = connect()


### define a function to reset the telescope between images
def reset_for_imaging(observation, safety_seconds=5):
    # move telescope
    telescope.go_to_j2000(observation["target_pos"][0], observation["target_pos"][1])
    time.sleep(safety_seconds)

    # change filter
    filterwheel.go_to("Empty")
    time.sleep(safety_seconds)

    # change focus
    focuser.go(filter_focus_dict[observation.get("filter_name")])
    time.sleep(safety_seconds)

    # configure camera
    camera.template = "{0}_{1}_{2}_{3}_{{seq:3}}_PY.fits".format(
        # observation.get("file_prefix"),
        observation.get("target_name").replace(" ", "-"),
        observation.get("filter_name"),
        str(observation.get("exp_time")).replace(".", "-"),)
    time.sleep(safety_seconds)

def do_observations():
    for observation in obs_list:
        # move the telescope to the observation target
        print("\nResetting telescope for new observation.")
        reset_for_imaging(observation)

        # get information for readout
        telescope_info = get_telescope_info(telescope)
        camera_info = get_camera_info(camera)
        filterwheel_info = get_filterwheel_info(filterwheel)
        focuser_info = get_focuser_info(focuser)

        # give readout
        print("Telescope configured for observing {0}.".format(observation["target_name"]))
        print("Moved telescope to {0}.".format(telescope_info["position"]))
        print("Set camera template to {0}.".format(camera_info["template"]))
        print("Set filter to {0}.".format(filterwheel_info["position"]))
        print("Set focuser to {0}.".format(focuser_info["position"]))

        # take the image
        # TODO: Integrate binning/cropping
        exp_time = observation.get("exp_time")
        print("Exposing for {0}".format(exp_time))
        camera.expose(exp_time)
        print("Exposure complete.")

        # check for end conditions
        if time.time() - start_time > obs_time*60*60:
            print("Reached maximum observation time of {0} hours.".format(obs_time))
            # return False to stop looping
            return False

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
        elif obs_loops >= obs_loop:
            print("Reached maximum loops of {0}.".format(obs_loop))
            break

    ### close telescope connections
    print("Imaging complete.")

else:
    print("Errors were found during obs_list check. Fix and re-run.")