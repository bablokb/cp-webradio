# ----------------------------------------------------------------------------
# channels.py: Manage radio stations.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# ----------------------------------------------------------------------------

from collections import namedtuple

from stations import channels

class Channels:
  """ List of channels """

  def __init__(self):
    """ constructor """

    Channel = namedtuple('Channel', 'nr name url logo')
    self._channels = []
    self.https = False
    for index, channel in enumerate(channels):
      self._channels.append(
        Channel(index,channel['name'],channel['url'],channel['logo']))
      if channel['url'].startswith('https'):
        self.https = True

    self._n = len(self._channels)
    self._current = 0

  def __getitem__(self, index: int):
    """ access by index """
    return self._channels[index]

  def current(self):
    """ return current channel """
    return self._channels[self._current]

  def set_current(self,name=None,nr=None):
    """ set current channel by name or number """

    if name is None and nr is None:
      raise ValueError("neither name nor nr specified")

    if name:
      for index, channel in enumerate(self._channels):
        if channel.name == name:
          self._current = index
          return channel
      raise ValueError(f"channel '{name}' not found")

    if 0 <= nr <= self._n:
      self._current = nr
      return self.current()
    else:
      ValueError(f"illegal channel-number {nr}")

  def name(self):
    """ return name of current channel """
    return self.current().name

  def url(self):
    """ return url of current channel """
    return self.current().url

  def next(self):
    """ return next channel """
    self._current = (self._current+1) % len(channels)
    return self.current()

  def prev(self):
    """ return prev channel """
    self._current = (self._current-1)
    if self._current < 0:
      self._current = len(channels)-1
    return self.current()

