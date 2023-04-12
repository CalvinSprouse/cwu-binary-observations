"""
Objective: Image the 44 Boo binary star system for a full period

https://en.wikipedia.org/wiki/44_Bo%C3%B6tis
Period: 6.43 Hours
Sys Min Mag: +6.40
Sys Max Mag: +5.8
Filter: V

These settings get us *just* the 6.43 hour period
More images before and after will be needed in order to ensure we get the period
If we have between 2130 and 430 (estimate) we have 7 hours
Total image time is ~90s after readout is considered
Makes for ~290 images to cover a 7 hour timespan which ideally includes eclipse

Image Interval: 60
Exposure Time: 20
Image Count: 290
"""

# imports
import astropy
import ace.syscore
import ace.camera
import ace.telescope
import astropy.coordinates as coord
import time
from astropy.coordinates import SkyCoord


# telescope is the name of the computer, Telescope is the telescope

# in seconds
astropy.utils.data.Conf.remote_timeout = 60
print "> Timeout:{0}".format(astropy.utils.data.Conf.remote_timeout)

# create a connection client
conn = ace.syscore.AceConnection("localhost")
conn.authenticate("root", "password")
print "> Connector authenticated"

# create a camera
camera = ace.camera.Camera(conn, "telescope", "FLI Camera")
print "> Camera created"

# create a telescope
telescope = ace.telescope.Telescope(conn, "telescope", "Telescope")
print "> Telescope created"


# observation configuration
# as found in stellarium
target_name = "44 Boo"
# in seconds
exposure_time = 20
# take an image _ seconds after the previous image
image_interval = 60
# take _ number of images
image_count = 290
# estimated duration
est_dur = image_count*(image_interval+exposure_time)
# estimated end time
est_fin = time.strftime("%H:%M", time.localtime(time.time() + est_dur))
# image save name
file_name_head = "44Boo"
# creat the save file template
file_template = "{0}_PY_{{seq:3}}.fits".format(file_name_head)
# get an initial position to confirm object name is good
target_pos = SkyCoord.from_name(target_name)

# readout observation configurations
print "> Complete Observation Configuration:"
print "Target Name:{0}".format(target_name)
print "Exposure Time:{0}".format(exposure_time)
print "Image Interval:{0}".format(image_interval)
print "Image Count:{0}".format(image_count)
print "Estimated Duration:{0}".format(est_dur)
print "Estimated Finish Time:{0}".format(est_fin)
print "File Header:{0}".format(file_name_head)
print "File Template:{0}".format(file_template)
print "Target Pos:{0}".format(target_pos)

# critical value check passed
print "> Observation Configuration Confirmed"

# configure computer
camera, telescope = computer_configuration()
print "> Complete Computer Configuration"

# configure camera file save tempalte
camera.template = file_template

# align telescope
print "> Moving Telescope: {0} @ {1}".format(target_name, target_pos))
telescope.go_to_j2000(target_pos.ra.degree, target_pos.dec.degree)

# begin exposure loop
for obs_count in range(image_count):
    print "> Exposing {0}. Image {1}".format(target_name, obs_count)
    camera.expose(exposure_time, x1=512, x2=1536, y1=512, y2=1536)
    print "> Exposure complete. Image {0}. Waiting {1}.".format(obs_count, image_interval)
    time.sleep(image_interval)

# end exposures and disconnect computer
print "> Imaging of {0} complete with {1} images.".format(target_name, obs_count)
camera = None
telescope = None
