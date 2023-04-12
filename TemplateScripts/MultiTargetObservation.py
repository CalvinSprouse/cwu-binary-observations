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

# define the observation orders
# orders are a dictionary of the following format
# ensure filters are the same as in initializer
# note that pause interval happens after exposure so the full elapsed time
# is exptime + readout_time + pause_interval
# before taking a new picture
# readouttime cannot be specified
observe_44_boo = {
    "target_name": "44 Boo",
    "file_name_prefix": "44Boo",

    "exposure_orders": {
        "Bessel U": {
            "count": 10,
            "exptime_seconds": 10,
            "pause_interval_seonds": 60,
            "last_exposure": 0
            },
    }
}

# load all observation orders into a list
observation_list = [
    observe_44_boo,
]

# test each observation order and sum the image counts
image_counts = 0
for index, observe in enumerate(observation_list):
    target_pos = SkyCoord.from_name(observe["target_name"])
    print("Position of {0} is {1}".format(
        observe["target_name"], target_pos))
    observation_list[index]["target_pos"] = target_pos

    for key, filter in observe["exposure_orders"].items():
        image_counts += filter["count"]

# begin observation loop
for obs_index in range(image_counts):
    print("Observation Index {0} of {1}".format(obs_index, image_counts))

    # find the next image that needs taking by scanning the observe orders for the lowest time to image
    lowest_time_to_image = time.time()
    next_index = (0, 0)

    for o_index, observe in enumerate(observation_list):
        for key, filter in observe["exposure_orders"].items():
            if filter["count"] <= 0: continue

            if time.time() - filter["last_exposure"]:
                lowest_time_to_image = time.time() - filter["last_exposure"]
                next_index = (o_index, key)

    print("Nearest image found to be in {0} seconds for {1}".format(
        lowest_time_to_image,
        observation_list[next_index[0]]["target_name"]
    ))

    # orient telescope to next target
    telescope.go_to_j2000(observation_list[next_index[0]]["target_pos"].ra.degree,
                          observation_list[next_index[0]]["target_pos"].dec.degree)

    # set the file format and load values from dict
    camera.template = observation_list[next_index[0]]["target_name_prefix"] + [next_index[1].replace(" ", "-")] + "_PY_{{seq:3}}.fits"
    exptime = observation_list[next_index[0]]["exposure_orders"][next_index[1]]["exptime_seconds"]

    # wait until ready
    while time.time() - observation_list[next_index[0]]["exposure_orders"][next_index[1]]["last_exposure"] < observation_list[next_index[0]]["exposure_orders"][next_index[1]]["pause_interval_seconds"]:
        time.sleep(0.1)

    # expose
    print("Exposing for {0} seconds to {1}".format(exptime, camera.template))
    camera.expose(exptime)
    print("Exposure complete saved to {0}".format(camera.template))

    # reduce img count and set last exposure
    observation_list[next_index[0]]["exposure_orders"][next_index[1]]["count"] -= 1
    observation_list[next_index[0]]["exposure_orders"][next_index[1]]["last_exposure"] = time.time()