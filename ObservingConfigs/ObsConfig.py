# configure the observation conditions

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
    {
        "target_name": "BZ Boo",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "V417 Boo",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "V336 Boo",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "V462 Dra",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "MX UMa",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "V384 UMa",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "V398 UMa",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel U",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel B",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel V",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel R",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },

    {
        "target_name": "W UMa",
        "filter_name": "Bessel I",
        "exp_time": 10,
        "img_count": 3,
        "pause_time": 30,
    },
]