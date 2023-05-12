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
    "Bessel B": -35556,
    "Bessel V": -34334,
    "Bessel R": -33844,
}

# obs_list defines the observations to do, the obs_list will be repeated
# as per obs_loop and run for obs_time (whichever expires first)
# each element of obs_list is an "observation" and is a dictionary
basic_pause = 5
img_count = 3
obs_list = [
    {
        "target_name": "BZ Boo",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "V417 Boo",
        "filter_name": "Bessel V",
        "exp_time": 12,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "V336 Boo",
        "filter_name": "Bessel V",
        "exp_time": 12,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "V462 Dra",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "MX UMa",
        "filter_name": "Bessel V",
        "exp_time": 8,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "V384 UMa",
        "filter_name": "Bessel V",
        "exp_time": 12,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "V398 UMa",
        "filter_name": "Bessel V",
        "exp_time": 12,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel V",
        "exp_time": 8,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel B",
        "exp_time": 16,
        "img_count": img_count,
        "pause_time": basic_pause,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel R",
        "exp_time": 4,
        "img_count": img_count,
        "pause_time": basic_pause,
    },
]