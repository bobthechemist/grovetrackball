"""
`btc_grove_trackball`
==============================================================

* Author(s): BoB LeSuer

Implementation Notes
--------------------

**Hardware:**

* `Grove Mini Track Ball <https://wiki.seeedstudio.com/Grove-Mini_Track_Ball/>`_

"""

import board
import time
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.1"
__repo__ = "TBD"

_GROVETRACKBALL_DEFAULT_ADDRESS = const(0x4a)
_GROVETRACKBALL_DEFAULT_CONFIG = const(0x3a6fb67c)

#enum CONFIG_REG_ADDR
CONFIG_REG_VALID = MOTION_REG_NUM = 5
CONFIG_REG_I2C_ADDR = CONFIG_REG_VALID + 4
CONFIG_REG_I2C_SPEED = 10
CONFIG_REG_LED_MODE = CONFIG_REG_I2C_SPEED + 2
CONFIG_REG_LED_FLASH_TIME = 13
CONFIG_REG_DATA_CLEAR_TIME = CONFIG_REG_LED_FLASH_TIME + 2
CONFIG_REG_DATA_READ_TIME = CONFIG_REG_DATA_CLEAR_TIME + 2
CONFIG_REG_NUM = CONFIG_REG_DATA_READ_TIME + 2

# LED modes
(
	LED_FLASH_1, LED_FLASH_2, LED_FLASH_TOGGLE, LED_FLASH_ALL,
	LED_ALWAYS_ON_1, LED_ALWAYS_ON_2,  LED_ALWAYS_ON_ALL, LED_ALWAYS_OFF,
	LED_BREATHING_1, LED_BREATHING_2, LED_BREATHING_ALL,
	LED_MOVE_FLASH,
	LED_MODE_NUM
) = range(13)


READ_MODE = 0
WRITE_MODE = 1

class GroveTrackball:
    """Interface to the Grove Mini Track Ball
    
    :param ~busio.I2C i2c_bus: The I2C bus the track ball is connected to.
    :param int address: The I2C address of the device. Defaults to :const:`0x4a`)
    
    **Quickstart**
    
    Here is an example of using the :class:`GroveTrackball` class.
    First you will need to import the libraries to use the track ball.
    
    .. code-block:: python
        import board
        import btc_grove_trackball
    
    Once this is done, you can define your `board.I2C` object and define the trackball object
    
    .. code-block:: python
    
        i2c = board.I2C()
        tb = btc_grove_trackball.GroveTrackBall(i2c)
    """
    
    def __init__(self, i2c_bus, address=_GROVETRACKBALL_DEFAULT_ADDRESS):
        self.dev = I2CDevice(i2c_bus, address)
        self.msg = bytearray(8)
    
    def write(self, reg: int, value: int):
        with self.dev as bus:
            bus.write(bytes([WRITE_MODE, reg, value]))
 
    def read(self, reg: int):
        with self.dev as bus:
            bus.write_then_readinto(bytes([READ_MODE, reg, 1]), self.msg, in_end=1)
        return self.msg[0]
    
    def led(self, led_mode: int):
        self.write(CONFIG_REG_LED_MODE, led_mode)

    def motion(self):
        return [self.read(i) for i in range(5)]
