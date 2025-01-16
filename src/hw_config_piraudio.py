# ----------------------------------------------------------------------------
# hw_config_piraudio.py: Hardware configuration for Pimoroni Pirate-Audio
#                        boards.
#
# Note that these boards are for the Pi, not the Pico and need an adapter
# that supports I2S. This file assumes the Pico-Zero-Base adapter from
# https://github.com/bablokb/pcb-pico-pi-base.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
#
# ----------------------------------------------------------------------------

import board
import busio
import displayio
from adafruit_st7789 import ST7789

PIN_TFT_CS   = board.GPIO7     # board.CE1
PIN_TFT_DC   = board.GPIO9     # board.MISO -> reuse unused pin
PIN_SPI_MOSI = board.GPIO10    # board.MOSI
PIN_SPI_CLK  = board.GPIO11    # board.SCLK

PIN_PREV     = board.GPIO6     # button B, lower left
PIN_NEXT     = board.GPIO20    # button Y, lower right (newer boards: GPIO24)
PIN_VOLDOWN  = board.GPIO5     # button A, upper left
PIN_VOLUP    = board.GPIO16    # button X, upper right

PIN_I2S_BCLK = board.GPIO18
PIN_I2S_WSEL = board.GPIO19
PIN_I2S_DATA = board.GPIO21

PIN_MUTE = board.GPIO25

class Settings:
  pass

# hardware configuration   ---------------------------------------------------

hw_config = Settings()
def _get_display():
  displayio.release_displays()

  spi = busio.SPI(PIN_SPI_CLK, PIN_SPI_MOSI)
  display_bus = displayio.FourWire(spi,
                                   command=PIN_TFT_DC, chip_select=PIN_TFT_CS)
  return ST7789(display_bus, width=240, height=240, rowstart=80, rotation=180)

def _get_keys():
  """ return list of pin-numbers for next, prev, volup, voldown """
  # format is (active-state,[next, prev, volup, voldown])
  return (False,[PIN_NEXT, PIN_PREV, PIN_VOLUP, PIN_VOLDOWN])

def _get_i2s_pins():
  return [PIN_I2S_BCLK,PIN_I2S_WSEL,PIN_I2S_DATA]

def _get_mute_pin():
  """ return mute pin """
  # format is (active-state,pin)
  return (False,PIN_MUTE)

hw_config.DISPLAY  = _get_display
hw_config.KEYS     = _get_keys
hw_config.I2S_PINS = _get_i2s_pins
hw_config.MUTE     = _get_mute_pin
