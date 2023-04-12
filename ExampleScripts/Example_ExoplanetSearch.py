import ace.syscore
import ace.camera
import ace.telescope
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
import astropy
import time

astropy.utils.data.Conf.remote_timeout = 60
conn = ace.syscore.AceConnection('localhost')
conn.authenticate('root', 'password')
camera = ace.camera.Camera(conn, 'telescope', 'FLI Camera')
#telescope is the name of the computer; Telescope is the name of the telescope
telescope = ace.telescope.Telescope(conn, 'telescope', 'Telescope')

#initial list of all stars being observed
#target_list = [('HAT-P-18','HAT-P18', 45), ('BD+44 2654','HAT-P67', 10), ('XO-3','XO-3', 4), ('Kepler-20','Kepler20', 40), ('Kepler-15','Kepler15', 105), ('HAT-P-32','HAT-P32', 26)]

#Rotation 1: 19:00-00:00
target_list = [('XO-3','XO-3', 4), ('HAT-P-32','HAT-P32', 26)]

#Rotation 2: 00:00-01:00
#target_list = [('XO-3','XO-3', 4)]

#Rotation 3: 01:00-02:00
#target_list = [('BD+44 2654','HAT-P67', 10), ('XO-3','XO-3', 4)]

#Rotation 4: 02:00-03:00
#target_list = [('HAT-P-18','HAT-P18', 45), ('BD+44 2654','HAT-P67', 10), ('XO-3','XO-3', 4)]

#Rotation 5: 03:00-06:00
#target_list = [('HAT-P-18','HAT-P18', 45), ('BD+44 2654','HAT-P67', 10), ('Kepler-20','Kepler20', 40), ('Kepler-15','Kepler15', 105)]

n_exposures = 3

loops = 63  #Rotation 1
#loops = 2  #Rotation 2
#loops = 2  #Rotation 3
#loops = 2  #Rotation 4
#loops = 6  #Rotation 5


#gather data for loops 0-loops
for i in xrange(loops):

        #for each star in the target list of this rotation
	for (target_name, save_name, exptime) in target_list:
#code adjusted to reflect better data collection techniques	for (target_name, save_name, ra, dec, exptime) in target_list:
		print 'Searching for', target_name
		pos = SkyCoord.from_name(target_name)
		print pos
		print 'Moving telescope to', target_name
		telescope.go_to_j2000(pos.ra.degree, pos.dec.degree)
		#code adjusted to reflect better data collection technique     telescope.go_to_j2000(ra, dec)
		print '... waiting'
		time.sleep(5) #wait 5 seconds
		s = '%s_{{seq:3}}.fits' % (save_name)
		#code adjusted to reflect better data collection technique     print 'Setting image filename template to:', s
		camera.template = s
		print 'Exposing. Surrender your data for the glory of the Sontaran Empire!!'
		for j in xrange(n_exposures):
                        print 'Image ', j+1
			camera.expose(exptime, x1=512, x2=1536, y1=512, y2=1536)
		print 'Images Taken'
		print ' '

	print ' '
	print 'Finished with loop ', i+1
	print ' '
	print 'Waiting.....Doctor......Who?......Doctor......Who?!'
	print ' '


	#time.sleep(1340) #Rotation 1
	#time.sleep(1490) #Rotation 2
	#time.sleep(1340) #Rotation 3
	#time.sleep(1190) #Rotation 4
	#time.sleep(1040) #Rotation 5

print 'Observations Complete'

camera = None
telescope = None
