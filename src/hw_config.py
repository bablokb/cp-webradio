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
               pin_tft_cs   = None,
               pin_tft_dc   = None,
               pin_spi_mosi = None,
               pin_spi_clk  = None,
               width        = 0,
               height       = 0,
               rowstart     = 0,
               rotation     = 0,

               pin_btn_prev    = None,
               pin_btn_next    = None,
               pin_btn_voldown = None,
               pin_btn_volup   = None,
               pin_btn_mute    = None,

               pin_i2s_bclk = None,
               pin_i2s_wsel = None,
               pin_i2s_data = None,
               pin_i2s_mute = None
               ):
    # TFT
    self.pin_tft_cs   = pin_tft_cs
    self.pin_tft_dc   = pin_tft_dc
    self.pin_spi_mosi = pin_spi_mosi
    self.pin_spi_clk  = pin_spi_clk
    self.width        = width
    self.height       = height
    self.rowstart     = rowstart
    self.rotation     = rotation

    # buttons
    self.pin_btn_prev    = pin_btn_prev
    self.pin_btn_next    = pin_btn_next
    self.pin_btn_voldown = pin_btn_voldown
    self.pin_btn_volup   = pin_btn_volup
    self.pin_btn_mute    = pin_btn_mute

    # I2S
    self.pin_i2s_bclk = pin_i2s_bclk
    self.pin_i2s_wsel = pin_i2s_wsel
    self.pin_i2s_data = pin_i2s_data
    self.pin_i2s_mute = pin_i2s_mute

  def get_display(self):
    """ display definition (override for non ST7789 displays) """
    displayio.release_displays()
    spi = busio.SPI(self.pin_spi_clk, self.pin_spi_mosi)
    display_bus = displayio.FourWire(
      spi,
      command=self.pin_tft_dc, chip_select=self.pin_tft_cs)
    return ST7789(display_bus, width=self.width,
                  height=self.height,
                  rowstart=self.rowstart, rotation=self.rotation)

  def get_keys(self):
    """ return list of pin-numbers for next, prev, volup, voldown, mute """
    # format is (active-state,[next, prev, volup, voldown, mute])
    return (False,[self.pin_btn_next,
                   self.pin_btn_prev,
                   self.pin_btn_volup,
                   self.pin_btn_voldown,
                   self.pin_btn_mute])

  def get_i2s_pins(self):
    return [self.pin_i2s_bclk,
            self.pin_i2s_wsel,
            self.pin_i2s_data,
            self.pin_i2s_mute]
