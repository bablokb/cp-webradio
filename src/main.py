# -------------------------------------------------------------------------
# Simple webradio with display (for station logos).
#
# This program needs an additional configuration file settings.py
# with wifi-credentials and application settings.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# -------------------------------------------------------------------------

import sys
import time
import keypad
import wifi
import gc

from settings import app_config, hw_config, secrets
DEBUG = getattr(app_config,'debug',False)

from channels import Channels
from player   import Player
from logo     import Logo

class Main:
  """ main-application class """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    # basic components
    self._logo  = Logo(hw_config.DISPLAY())
    self._channels = Channels()
    self._player   = Player(hw_config.I2S_PINS(),
                            app_config.bufsize,
                            self._channels.https)
    self._playing = False
    self._muted   = False

    # setup keys and navigation
    keys = hw_config.KEYS()
    self._keys = keypad.Keys(keys[1],
                             value_when_pressed=keys[0],pull=True,
                             interval=0.1,max_events=4)
    self._key_events = self._keys.events
    self._key_callbacks = [
      self._on_next,self._on_prev,self._on_volup,self._on_voldown]
    if len(keys) == 5:
      self._key_callbacks.append(self._on_mute)

  # --- print debug-message   ------------------------------------------------

  def msg(self,text):
    """ print (debug) message """
    if DEBUG:
      print(text)

  # --- connect to network   -------------------------------------------------

  def _connect(self):
    """ connect to wifi """

    self.msg(f"connecting to AP {secrets.ssid} ...")
    timeout = getattr(secrets,'timeout',5)
    retries = getattr(secrets,'retries',3)

    state = wifi.radio.connected
    print(f"  connected: {state}")
    if state:
      return

    for _ in range(retries):
      try:
        wifi.radio.connect(secrets.ssid,
                           secrets.password,
                           timeout = timeout
                           )
        break
      except ConnectionError as ex:
        self.msg(f"{ex}")
    self.msg(f"  connected: {wifi.radio.connected}")
    if not wifi.radio.connected:
      raise ConnectionError(f"could not connect to {secrets.ssid}")

  # --- play a given channel   -----------------------------------------------

  def _play(self,channel):
    """ play given channel """

    # stop last channel
    self.msg("stopping player")
    self._muted = True
    self._player.mute(self._muted)
    self._player.stop()
    self._playing = False
    self.msg(f"_play: free memory after stop(): {gc.mem_free()}")

    # update logo
    self._logo.show(channel)

    # start given channel
    self.msg(f"playing {channel.name}")
    if self._player.play(channel.url):
      self._playing = True
      self._muted = False
      self._player.mute(self._muted)
      self.msg(f"_play: free memory after play(): {gc.mem_free()}")
    else:
      self._logo.show(img="error")

  # --- navigation callback: prev   ------------------------------------------

  def _on_prev(self):
    """ play previous song in list """
    channel = self._channels.prev()
    self._play(channel)

  # --- navigation callback: next   ------------------------------------------

  def _on_next(self):
    """ play next song in list """
    channel = self._channels.next()
    self._play(channel)

  # --- navigation callback: volume up   -------------------------------------

  def _on_volup(self):
    """ increase volume """
    pass

  # --- navigation callback: volume down   -----------------------------------

  def _on_voldown(self):
    """ decrease volume """
    pass

  # --- navigation callback: mute   ------------------------------------------

  def _on_mute(self):
    """ mute player """
    self._muted = not self._muted
    self._player.mute(self._muted)

  # --- main loop   ----------------------------------------------------------

  def run(self):
    """ main-loop """

    # connect to WLAN
    self._connect()

    # check for autoplay
    if hasattr(app_config,"autoplay"):
      # set channel and play it
      self._channels.set_current(app_config.autoplay)
      channel = self._channels.current()
      self._play(channel)
    else:
      # select last channel, wait for 'next' to play it
      self._channels.prev()

    while True:
      event = self._key_events.get()
      if event and event.pressed:
        self._key_callbacks[event.key_number]()
      if self._playing and not self._player.playing:
        # we are into trouble
        self.msg("player not playing...")
        self.playing = False
        self._logo.show(img="error")
      time.sleep(0.2)

# --- main application code   -------------------------------------------------

app = Main()
app.run()
