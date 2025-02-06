# ----------------------------------------------------------------------------
# hw_config_qtpy_esp32s3.py: ESP32-S3 QT-Py with EYESPI-BFF and Audio-BFF.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# ----------------------------------------------------------------------------

import board
from hw_config import HWConfig

PIN_TFT_CS   = board.TX
PIN_TFT_DC   = board.RX
PIN_TFT_BL   = board.A0
PIN_SPI_MOSI = board.MOSI
PIN_SPI_CLK  = board.SCK
WIDTH        = 240
HEIGHT       = 320
ROTATION     = 180

PIN_BTN_PREV    = board.D41     # SDA1 (SDA on Stemma/Qt)
PIN_BTN_NEXT    = board.D40     # SCL1 (SCL on Stemma/Qt)
PIN_BTN_RELOAD  = board.D0      # boot-button
PIN_BTN_MUTE    = board.A4      # unused

PIN_I2S_BCLK = board.A3
PIN_I2S_WSEL = board.A2
PIN_I2S_DATA = board.A1
PIN_I2S_MUTE = None

class Config(HWConfig):
  def __init__(self):
    super().__init__(
      # TFT
      tft_pins = [PIN_TFT_CS, PIN_TFT_DC, PIN_SPI_MOSI, PIN_SPI_CLK],
      tft_parms = {"baudrate": 60_000_000,
                   "width": WIDTH, "height": HEIGHT,
                   "backlight_pin": PIN_TFT_BL,
                   "rotation": ROTATION},
      # buttons
      btn_pins = [PIN_BTN_PREV, PIN_BTN_NEXT,
                  PIN_BTN_RELOAD, PIN_BTN_MUTE],
      # I2S
      i2s_pins = [PIN_I2S_BCLK, PIN_I2S_WSEL, PIN_I2S_DATA, PIN_I2S_MUTE]
      )

hw_config = Config()
