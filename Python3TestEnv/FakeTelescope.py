# imports
import time
from enum import Enum

from astropy.coordinates import SkyCoord
from rich import print

# note: only emulating used functions

# create the telescope class
class Conn:
    def __init__(self, location: str):
        # expected to be "localhost"
        self.location = location
        self.user = None
        self.password = None

        print(f"Created Conn @ {self.location}.")

    def authenticate(self, user: str, password: str):
        # expected to be "root" "password"
        self.user = user
        self.password = password

        print(f"Authenticated {self.user} {self.password}.")


# create the camera class
class CameraState(Enum):
    IDLE = "IDLE"
    EXPOSING = "EXPOSING"
    PAUSED = "PAUSED"

class CameraExposureType(Enum):
    LIGHT = "LIGHT"
    FLAT = "FLAT"
    DARK = "DARK"
    BIAS = "BIAS"
    SKYFLAT = "SKYFLAT"

class Camera:
    def __init__(self, conn: Conn, instrument_name: str, camera_name: str):
        # expected to be conn, "telescope", "FLI Camera"
        self.conn = conn
        self.instrument_name = instrument_name
        self.camera_name = camera_name

        # initializations
        self.state = CameraState.IDLE
        self.exposure_type = None
        self.temperature = 0
        self.setpoint = 0
        self.readout_mode = None
        self.can_pause = False
        self.template = ".fits"

        print(f"Created Camera with {self.conn}, {self.instrument_name}, {self.camera_name}.")

    def expose(self, exptime: float, type: CameraExposureType = CameraExposureType.LIGHT, bin_x: int = 1, bin_y: int = 1, x1: int = 1, x2: int = 1, y1: int = 1, y2:int = 1, overscan = 0, save: bool = True, block: bool = True):
        print(f"Imaging {type} for {exptime} seconds with bins ({bin_x}, {bin_y}) crops (({x1}, {y1}), ({x2}, {y2})) overscan {overscan}, save {save}, block {block}.")

        self.can_pause = True
        time.sleep(exptime)
        self.can_pause = False

        if save: print(f"Image saved as {self.template}.")


# create the telescope class
class RaDecPosition:
    def __init__(self, ra, dec):
        self.ra = ra
        self.dec = dec

class Telescope:
    def __init__(self, conn: Conn, instrument_name: str, telescope_name):
        # expected to be conn "telescope" "Telescope"
        self.conn = conn
        self.instrument_name = instrument_name
        self.telescope_name = telescope_name

        print(f"Created Telescope with {self.conn}, {self.instrument_name}, {self.telescope_name}.")

    def go_to_j2000(self, ra, dec):
        pass

    def get_target():
        pass

    def get_position():
        pass


# create the dome class
class DomeState(Enum):
    AJAR = "AJAR"
    CLOSED = "CLOSED"
    CLOSING = "CLOSING"
    ERROR = "ERROR"
    OPEN = "OPEN"
    OPENING = "OPENING"
    SLEWING = "SLEWING"
    TRACKING = "TRACKING"

class Dome:
    def __init__(self, conn: Conn, instrument_name: str, dome_name: str):
        # expected conn, "telescope", "Dome"
        self.conn = conn
        self.instrument_name = instrument_name
        self.dome_name = dome_name

        # initialization
        self.azimuth = 128
        self.cmd_azimuth = 0
        self.cmd_elevation = 0
        self.parkk_azimuth = 128
        self.state = DomeState.CLOSED

        print(f"Created Dome with {self.conn}, {self.instrument_name}, {self.dome_name}.")

    def open():
        pass

    def close():
        pass

    def stop():
        pass


# create the filterwheel class
class FilterWheelState(Enum):
    UNKOWN = "UNKOWN"
    STOPPED = "STOPPED"
    INITIALIZING = "INITIALIZING"
    MOVING = "MOVING"
    FAULT = "FAULT"

class FilterWheel:
    def __init__(self, conn: Conn, instrument_name: str, filterwheel_name: str):
        # expected conn, "telescope", "Filter Wheel"
        self.conn = conn
        self.instrument_name = instrument_name
        self.filterwheel_name = filterwheel_name

        # hard code filter options
        # TODO
        self.filters = ["A"]

        # initialization
        self.state = FilterWheelState.STOPPED
        self.position = 0
        self.positions = len(self.filters)
        self.filter_name = self.filters[self.position]
        self.target = self.position

        print(f"Created FilterWheel with {self.conn}, {self.instrument_name}, {self.filterwheel_name}.")

    def go_to(self, pos):
        pass

    def init(self):
        pass

    def get_names(self):
        return self.filters


# define focuser class
class FocuserState(Enum):
    LIMIT_FWD = "LIMIT_FWD"
    LIMIT_REV = "LIMIT_REV"
    MOVING_FWD = "MOVING_FWD"
    MOVING_REV = "MOVING_REV"
    STOPPED = "STOPPED"

class Focuser:
    def __init__(self, conn: Conn, instrument_name: str, focuser_name: str):
        # expected conn, "telescope", "Main Focus"
        self.conn = conn
        self.instrument_name = instrument_name
        self.focuser_name = focuser_name

        # initialization
        self.state = FocuserState.STOPPED
        self.position = 0
        self.target = self.position
        self.minimum = -100000
        self.maxium = -self.minimum

        print(f"Created Focuser with {self.conn}, {self.instrument_name}, {self.focuser_name}.")

    def go(pos):
        pass

    def go_to_minimum():
        pass

    def go_to_maximum():
        pass

    def stop():
        pass