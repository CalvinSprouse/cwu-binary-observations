# Python Version: 2

# configure the observation conditions

# number of hours change from UTC, only changes with PDT vs PST time change
utc_offset = -7

# obs_loop controls the maximum number of iterations
# 0 = infinite
obs_loop = 0

# obs_time controls the maximum duration to run the observation in hours
# must be some non-zero number (failsafe)
# 2 hours is a good limit beyond which the lenses may require re-focusing
obs_time = 2

# obs_pause controls how long to pause between loops in seconds
obs_pause = 1*60

# configure the focus wheel values
# add in any filter that will be used as a key
# and the value of the focus wheel as a value
filter_focus_dict = {
    "Empty": 0,
    "Bessel U": 0,
    "Bessel B": 0,
    "Bessel V": 0,
    "Bessel R": 0,
    "Bessel I": 0,
    "H Alpha": 0,
    "H Beta": 0,
    "O_III": 0,
    "S_II": 0,
}

# obs_list defines the observations to do, the obs_list will be repeated
# as per obs_loop and run for obs_time (whichever expires first)
# each element of obs_list is an "observation" and is a dictionary
obs_list = [
]


# here is an example obs list
# the first element is the raw form and can be copied over
# the second element is an actual observation that could be used
example_obs_list = [
    # this dictionary represents a single observing event
    # copy and paste multiple of these dictionaries for multiple observing events
    {
        # the name of the target as used by astropy to find ra/dec
        "target_name":"",

        # the name of the filter as used by the telescope (see Initializer.py for names)
        "filter_name":"",

        # the exposure time in seconds
        "exp_time":"",

        # the number of images to take, if more than 1 they will be back-to-back with a 1 second pause (optional, default=1)
        "img_count":"",

        # the time to pause after this observation in seconds (optional, default=1)
        "pause_time":"",

        # a custom prefix to put in front of files
        # note that files will be named like
        # [prefix]_[target]_[filter]_[exposure]_[sequence]_PY.fits
        "file_prefix":"",

        # a way to override the target_name, if empty will use the astropy name (optional)
        # but if full will use this given position
        # target position is a tuple of (ra, dec) both in degrees
        "target_pos":(),

        # send binning information for the camera (optional)
        # if none then no binning will be used
        # binning is a tuple of (x_lim, y_lim)
        "binning":(),

        # send cropping information for the camera (optional)
        # if non then no cropping will be used
        # cropping is a tuple of (min_x, min_y, max_x, max_y)
        "cropping":(),
     },

    # notice in this example the optional parameters are not set
    {
        "target_name": "44 Boo",
        "filter_name": "Bessel B",
        "exp_time": 1,
        "img_count": 3,
        "pause_time": 5*60,
     },
]