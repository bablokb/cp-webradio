# -------------------------------------------------------------------------
# logo.py: Display logo/name on the display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
# -------------------------------------------------------------------------

import gc
import displayio
import terminalio
from adafruit_display_text.bitmap_label import Label

class Logo:
  """ class Logo """

  def __init__(self,display):
    """ constructor """
    self._display = display
    self._group   = displayio.Group()
    self._text    = None
    self._display.root_group = self._group
    self._display.auto_refresh = False

  # --- show logo or name   --------------------------------------------------

  def show(self,channel,img=None):
    """ load and show logo. Pass img to show explicit bmp (e.g. error) """

    if img:
      logo_path = f"/logos/{img}.bmp"
    else:
      logo_path = f"/logos/{channel.logo}.bmp"
    try:
      self._show_image(logo_path)
    except Exception as ex:
      print(f"logo {logo_path} not found (exception: {ex})")
      self._show_name(img if img else channel.name)

  # --- show image   ---------------------------------------------------------

  def _show_image(self,path):
    """ load logo-image as TileGrid """

    if len(self._group):
      del self._group[0]
      gc.collect()

    f = open(path, "rb")
    pic = displayio.OnDiskBitmap(f)
    x = int((self._display.width-pic.width)/2)
    y = int((self._display.height-pic.height)/2)
    t = displayio.TileGrid(pic, x=x,y=y, pixel_shader=pic.pixel_shader)
    self._group.insert(0,t)
    self._display.refresh()

  # --- show name   ----------------------------------------------------------

  def _show_name(self,name):
    """ show station name as text """

    if self._text:
      self._text.text = name
      return

    self._text = Label(terminalio.FONT,text=name)
    self._text.anchor_point = (0.5,0.5)
    self._text.anchored_position = (self._display.width//2,
                                    self._display.height//2)
    self._group.insert(0,self._text)
    self._display.refresh()
