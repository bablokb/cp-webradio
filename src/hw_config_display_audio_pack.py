# ----------------------------------------------------------------------------
# hw_config_display_audiopack.py
#
# Hardware configuration using the
# Pimoroni Pico Display-Pack (https://shop.pimoroni.com/products/pico-display-pack)
# Pimoroni Pico Audio-Pack (https://shop.pimoroni.com/products/pico-audio-pack)
#
# This combination needs a pin-multiplexer.
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

PIN_TFT_CS   = board.GP17
PIN_TFT_DC   = board.GP16
PIN_SPI_MOSI = board.GP19
PIN_SPI_CLK  = board.GP18
PIN_BL       = board.GP20

PIN_BTN_PREV     = board.GP13      # button B, lower left
PIN_BTN_NEXT     = board.GP15      # button Y, lower right
PIN_BTN_VOLDOWN  = board.GP12      # button A, upper left
PIN_BTN_VOLUP    = board.GP14      # button X, upper right
PIN_BTN_MUTE    = None

PIN_I2S_BCLK = board.GP10
PIN_I2S_WSEL = board.GP11
PIN_I2S_DATA = board.GP9
PIN_I2S_MUTE = board.GP22

class Settings:
  pass

# hardware configuration   ---------------------------------------------------

hw_config = Settings()
def _get_display():
  displayio.release_displays()

  spi = busio.SPI(PIN_SPI_CLK, PIN_SPI_MOSI)
  display_bus = displayio.FourWire(spi,
                                   command=PIN_TFT_DC, chip_select=PIN_TFT_CS)
  display = ST7789(display_bus, width=240, height=135, backlight_pin=PIN_BL,
                   rowstart=40, colstart=53, rotation=270)
  display.brightness = 0.8
  return display

def _get_keys():
  """ return list of pin-numbers for next, prev, volup, voldown """
  # format is (active-state,[next, prev, volup, voldown])
  return (False,[PIN_BTN_NEXT, PIN_BTN_PREV, PIN_BTN_VOLUP, PIN_BTN_VOLDOWN])

def _get_i2s_pins():
  return [PIN_I2S_BCLK,PIN_I2S_WSEL,PIN_I2S_DATA,PIN_I2S_MUTE]

hw_config.DISPLAY  = _get_display
hw_config.KEYS     = _get_keys
hw_config.I2S_PINS = _get_i2s_pins
