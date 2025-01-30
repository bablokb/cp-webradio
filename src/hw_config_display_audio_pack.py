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
# ----------------------------------------------------------------------------

import board
from hw_config import HWConfig

PIN_TFT_CS   = board.GP17
PIN_TFT_DC   = board.GP16
PIN_SPI_MOSI = board.GP19
PIN_SPI_CLK  = board.GP18
PIN_BL       = board.GP20
WIDTH        = 240
HEIGHT       = 135
ROWSTART     = 40
COLSTART     = 53
ROTATION     = 270
BRIGHTNESS   = 0.8

PIN_BTN_PREV   = board.GP13      # button B, lower left
PIN_BTN_NEXT   = board.GP15      # button Y, lower right
PIN_BTN_RELOAD = board.GP12      # button A, upper left
PIN_BTN_MUTE   = board.GP14      # button X, upper right

PIN_I2S_BCLK = board.GP10
PIN_I2S_WSEL = board.GP11
PIN_I2S_DATA = board.GP9
PIN_I2S_MUTE = board.GP22

class Config(HWConfig):
  def __init__(self):
    super().__init__(
      # TFT
      tft_pins = [PIN_TFT_CS, PIN_TFT_DC, PIN_SPI_MOSI, PIN_SPI_CLK, PIN_BL],
      tft_parms = {"baudrate": 60_000_000,
                   "width": WIDTH, "height": HEIGHT,
                   "rowstart": ROWSTART, "colstart": COLSTART,
                   "rotation": ROTATION, "brightness": BRIGHTNESS},
      # buttons
      btn_pins = [PIN_BTN_PREV, PIN_BTN_NEXT,
                  PIN_BTN_RELOAD, PIN_BTN_MUTE],
      # I2S
      i2s_pins = [PIN_I2S_BCLK, PIN_I2S_WSEL, PIN_I2S_DATA, PIN_I2S_MUTE]
      )

hw_config = Config()
