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
# ----------------------------------------------------------------------------

import board
from hw_config import HWConfig

PIN_TFT_CS   = board.GPIO7     # board.CE1
PIN_TFT_DC   = board.GPIO9     # board.MISO -> reuse unused pin
PIN_SPI_MOSI = board.GPIO10    # board.MOSI
PIN_SPI_CLK  = board.GPIO11    # board.SCLK
WIDTH        = 240
HEIGHT       = 240
ROWSTART     = 80
ROTATION     = 180

PIN_BTN_PREV    = board.GPIO6     # button B, lower left
PIN_BTN_NEXT    = board.GPIO20    # button Y, lower right (newer boards: GPIO24)
PIN_BTN_RELOAD  = board.GPIO5     # button A, upper left
PIN_BTN_MUTE    = board.GPIO16    # button X, upper right

PIN_I2S_BCLK = board.GPIO18
PIN_I2S_WSEL = board.GPIO19
PIN_I2S_DATA = board.GPIO21
PIN_I2S_MUTE = board.GPIO25

class Config(HWConfig):
  def __init__(self):
    super().__init__(
      # TFT
      tft_pins = [PIN_TFT_CS, PIN_TFT_DC, PIN_SPI_MOSI, PIN_SPI_CLK],
      tft_parms = {"baudrate": 60_000_000,
                   "width": WIDTH, "height": HEIGHT,
                   "rowstart": ROWSTART, "rotation": ROTATION},
      # buttons
      btn_pins = [PIN_BTN_PREV, PIN_BTN_NEXT,
                  PIN_BTN_RELOAD, PIN_BTN_MUTE],
      # I2S
      i2s_pins = [PIN_I2S_BCLK, PIN_I2S_WSEL, PIN_I2S_DATA, PIN_I2S_MUTE]
      )

hw_config = Config()
