# ----------------------------------------------------------------------------
# hw_config_waveshare_13.py
#
# Hardware configuration using the
# Waveshare Pico LCD 1.3 (see https://www.waveshare.com/wiki/Pico-LCD-1.3)
# and an external I2S-breakout connected to GP6, GP7, GP5.
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

PIN_TFT_CS   = board.GP9
PIN_TFT_DC   = board.GP8
PIN_SPI_MOSI = board.GP11
PIN_SPI_CLK  = board.GP10

PIN_BTN_PREV    = board.GPI6      # joystick left
PIN_BTN_NEXT    = board.GP20      # joystick right
PIN_BTN_VOLDOWN = board.GP18      # joystick down
PIN_BTN_VOLUP   = board.GP2       # joystick up
PIN_BTN_MUTE    = board.GP18      # joystick down

PIN_I2S_BCLK = board.GP6
PIN_I2S_WSEL = board.GP7
PIN_I2S_DATA = board.GP5
PIN_I2S_MUTE = board.GP4

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
  return (False,[PIN_BTN_NEXT, PIN_BTN_PREV,
                 PIN_BTN_VOLUP, PIN_BTN_VOLDOWN, PIN_BTN_MUTE])

def _get_i2s_pins():
  return [PIN_I2S_BCLK,PIN_I2S_WSEL,PIN_I2S_DATA,PIN_I2S_MUTE]

hw_config.DISPLAY  = _get_display
hw_config.KEYS     = _get_keys
hw_config.I2S_PINS = _get_i2s_pins
