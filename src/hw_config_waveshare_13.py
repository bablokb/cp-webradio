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
# ----------------------------------------------------------------------------

import board
from hw_config import HWConfig

PIN_TFT_CS   = board.GP9
PIN_TFT_DC   = board.GP8
PIN_SPI_MOSI = board.GP11
PIN_SPI_CLK  = board.GP10
PIN_TFT_BL   = board.GP13
PIN_TFT_RST  = board.GP12

WIDTH        = 240
HEIGHT       = 240
ROWSTART     = 80
ROTATION     = 270

PIN_BTN_PREV   = board.GP16      # joystick left
PIN_BTN_NEXT   = board.GP20      # joystick right
PIN_BTN_RELOAD = board.GP19      # key X
PIN_BTN_MUTE   = board.GP21      # key Y

PIN_I2S_BCLK = board.GP6
PIN_I2S_WSEL = board.GP7
PIN_I2S_DATA = board.GP5
PIN_I2S_MUTE = board.GP4

class Config(HWConfig):
  def __init__(self):
    super().__init__(
      # TFT
      tft_pins = [PIN_TFT_CS, PIN_TFT_DC, PIN_SPI_MOSI,
                  PIN_SPI_CLK, PIN_TFT_RST],
      tft_parms = {"baudrate": 60_000_000,
                   "width": WIDTH, "height": HEIGHT,
                   "rowstart": ROWSTART, "rotation": ROTATION,
                   "backlight_pin": PIN_TFT_BL
      },
      # buttons
      btn_pins = [PIN_BTN_PREV, PIN_BTN_NEXT,
                  PIN_BTN_RELOAD, PIN_BTN_MUTE],
      # I2S
      i2s_pins = [PIN_I2S_BCLK, PIN_I2S_WSEL, PIN_I2S_DATA, PIN_I2S_MUTE]
      )

  def get_icon_offsets(self):
    """ return offsets for icons on the screen """

    return [None,             # left of logo  (prev)
            None,             # right of logo (next)
            (-1,0.60),        # middle right  (reload)
            (-1,0.80)]        # bottom right  (mute)

hw_config = Config()
