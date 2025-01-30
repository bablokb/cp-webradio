# ----------------------------------------------------------------------------
# hw_config.py: Implements HWConfig, the base class for hardware-configurations.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# ----------------------------------------------------------------------------

import busio
import displayio
from adafruit_st7789 import ST7789

class HWConfig:
  def __init__(self,
               tft_driver = ST7789,
               tft_pins = [None]*4,
               tft_parms = {},
               btn_pins = [None]*4,
               btn_active = False,
               i2s_pins = [None]*3,
               ):
    # TFT (backlight-pin is optional)
    self._tft_driver = tft_driver
    self._tft_parms  = tft_parms
    (self.pin_tft_cs, self.pin_tft_dc,
     self.pin_spi_mosi, self.pin_spi_clk) = tft_pins[:4]
    if len(tft_pins) == 5:
      self.pin_tft_rst = tft_pins[4]
    else:
      self.pin_tft_rst = None

    # buttons
    self._active  = btn_active
    self._buttons = btn_pins[:4]

    # I2S (mute pin is optional)
    self._i2s_pins = i2s_pins[:3]
    if len(i2s_pins) == 4:
      self._i2s_pins.append(i2s_pins[3])
    else:
      self._i2s_pins.append(None)

  def get_display(self):
    """ display definition """
    displayio.release_displays()
    spi = busio.SPI(self.pin_spi_clk, self.pin_spi_mosi)
    if "baudrate" in self._tft_parms:
      if spi.try_lock():
        spi.configure(baudrate=self._tft_parms["baudrate"])
        spi.unlock()
      del self._tft_parms["baudrate"]
    display_bus = displayio.FourWire(spi,
                                     command=self.pin_tft_dc,
                                     chip_select=self.pin_tft_cs,
                                     reset=self.pin_tft_rst)
    return self._tft_driver(display_bus,**self._tft_parms)

  def get_keys(self):
    """ return list of pin-numbers for prev, next, reload, mute

    Format: (active-state,[prev, next, reload, mute])
    """
    return (self._active,self._buttons)

  def get_i2s_pins(self):
    return self._i2s_pins

  def get_icon_offsets(self):
    """ return offsets for icons on the screen

    Format:  [(x-off,y-off),...] for every button in the same order as
             get_keys()
    A negative x-offset is from the right boarder, a negative y-offset
    is from the bottom. If 0 < abs(offset) < 1, then it is interpreted as
    a fraction of width/height.
    """
    return [(1,-0.25),       # lower left  (prev)
            (-1,-0.25),      # lower right (next)
            (1,0.25),        # upper left  (reload)
            (-1,0.25)]       # upper right (mute)
