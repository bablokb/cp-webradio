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

    # save app_config
    self.config = app_config

    # basic components
    display = hw_config.get_display()
    if display:
      self._logo = Logo(display,
                        hw_config.get_icon_offsets(),
                        hw_config.extra_icons())
    else:
      self._logo = None
    self.channels = Channels()
    self._player   = Player(hw_config.get_i2s_pins(),
                            app_config.bufsize,
                            self.channels.https)
    self._playing  = None
    self._muted    = False
    self._start_at = None

    # setup keys and navigation
    keys = hw_config.get_keys()
    self._keys = keypad.Keys(keys[1],
                             value_when_pressed=keys[0],pull=True,
                             interval=0.1,max_events=4)
    self._key_events = self._keys.events
    self._key_callbacks = [
      self.on_prev,self.on_next,self.on_reload,self.on_mute]

    # add callback for extra keys (delegate to hw_config)
    for _ in range(4,len(keys[1])):
      self._key_callbacks.append(hw_config.on_key)

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
      self._logo and self._logo.show(img="error")
      raise ConnectionError(f"could not connect to {secrets.ssid}")

  # --- stop playing   -------------------------------------------------------

  def stop(self):
    """ stop current playback """

    self.msg("stopping player")
    self._muted = True
    self._player.mute(self._muted)
    self._player.stop()
    self._playing = None
    self.msg(f"stop: free memory after stop(): {gc.mem_free()}")

  # --- start playing   ------------------------------------------------------

  def _start(self,channel=None):
    """ start playing current or given channel """

    # start given channel
    self._start_at = None
    if not channel:
      channel = self.channels.current()

    self.msg(f"playing {channel.name}")
    if self._player.play(channel.url):
      self._playing = time.monotonic()
      self._muted = False
      self._player.mute(self._muted)
      self.msg(f"_start: free memory after play(): {gc.mem_free()}")
    else:
      self._logo and self._logo.show(img="error")

  # --- play a given channel   -----------------------------------------------

  def play(self,channel):
    """ play given channel """

    # stop current playback
    self.stop()

    # update logo
    self._logo and self._logo.show(channel)
    if not app_config.switch_delay:
      # start now
      self._start(channel)
    else:
      # schedule start in a few seconds
      self._start_at = time.monotonic() + app_config.switch_delay
      self.msg(f"play: start of {channel.name} in {app_config.switch_delay}s")

  # --- navigation callback: prev   ------------------------------------------

  def on_prev(self):
    """ play previous song in list """
    channel = self.channels.prev()
    self.play(channel)

  # --- navigation callback: next   ------------------------------------------

  def on_next(self):
    """ play next song in list """
    channel = self.channels.next()
    self.play(channel)

  # --- navigation callback: volume down   -----------------------------------

  def on_reload(self):
    """ reload channel """
    channel = self.channels.current()
    self.play(channel)

  # --- navigation callback: mute   ------------------------------------------

  def on_mute(self):
    """ mute player """
    self._muted = not self._muted
    self._player.mute(self._muted)

  # --- main loop   ----------------------------------------------------------

  def run(self):
    """ main-loop """

    # connect to WLAN
    self._logo and self._logo.show(img="wlan")
    self._connect()

    # check for autoplay
    if hasattr(app_config,"autoplay"):
      # set channel and play it
      self.play(self.channels.set_current(app_config.autoplay))
    else:
      # select last channel, wait for 'next' to play it
      self.channels.prev()
      self._logo and self._logo.show(img="radio")

    while True:
      # check for button
      event = self._key_events.get()
      if event and event.pressed:
        if event.key_number < 4:
          self._key_callbacks[event.key_number]()
        else:
          self._key_callbacks[event.key_number](event.key_number,self)

      # check for scheduled start
      if self._start_at and time.monotonic() > self._start_at:
        self._start()

      # check for error condition
      if (self._playing and
          time.monotonic()-self._playing > app_config.max_wait and
          not self._player.playing):
        # we are into trouble
        self.msg(f"player not playing since {app_config.max_wait}s ...")
        self._playing = None
        self._logo and self._logo.show(img="error")
      time.sleep(0.2)

# --- main application code   -------------------------------------------------

app = Main()
app.run()
