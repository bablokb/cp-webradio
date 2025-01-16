# ----------------------------------------------------------------------------
# player.py: The class Player connects to a webradio station and streams the
#            MP3-data from an URL to an I2S-device.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# ----------------------------------------------------------------------------

import time
import gc

import board
import digitalio
import audiobusio
import audiomp3

import wifi
import socketpool
import ssl
import adafruit_requests

class Player:
  """ Player for webradio """

  def __init__(self,i2s_pins,mute_pin,bufsize,use_ssl=False):
    """ constructor """
    self._buffer  = bytearray(bufsize)
    self._decoder = audiomp3.MP3Decoder("dummy.mp3", self._buffer)
    self._i2s     = audiobusio.I2SOut(*i2s_pins)

    if mute_pin[1]:
      # create mute-pin and start muted
      self._mute = (mute_pin[0],digitalio.DigitalInOut(mute_pin[1]))
      self._mute[1].switch_to_output(value=mute_pin[0])
    else:
      self._mute = None
      
    pool = socketpool.SocketPool(wifi.radio)
    if use_ssl:
      self._requests = adafruit_requests.Session(
        pool,
        ssl.create_default_context())
    else:
      self._requests = adafruit_requests.Session(pool)

  # --- play the given webradio-station   ------------------------------------

  def play(self,url):
    """ stream from the given url """

    gc.collect()
    while True:
      try:
        self._response = self._requests.get(
          url,
          headers = {"connection": "close"},
          stream = True)
        if not self._response:
          print(f"no response for {url}")
          time.sleep(1)
          continue
        self._decoder.file = self._response.socket
        self._i2s.play(self._decoder)
        return True
      except Exception as ex:
        print(f"play(): exeception: {ex}")
        return False

  # --- stop playing   -------------------------------------------------------

  def stop(self):
    """ stop playing radio stream """
    if self._i2s.playing:
      try:
        self._i2s.stop()
        self._response.socket.close()
        self._response.close()
      except Exception as ex:
        print(f"stop(): exeception: {ex}")

  # --- mute   ---------------------------------------------------------------

  def mute(self,value):
    """ drive mute-pin: value=True is mute """

    if self._mute:
      if not self._mute[0]:
        # active low, so change
        value = not value
      self._mute[1].value = value
