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
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.bitmap_label import Label

IFONT = "fonts/open-iconic-24.bdf"
ICONS = ["\uE097",  # media-step-backward
         "\uE098",  # media-step-forward
         "\uE0B3",  # reload
         "\uE0A1"]  # musical-note

class Logo:
  """ class Logo """

  def __init__(self,display,offsets):
    """ constructor """
    self._display = display
    self._display.auto_refresh = False

    self._group   = displayio.Group()
    self._text    = None
    self._display.root_group = self._group

    # add buttons
    ifont = bitmap_font.load_font(IFONT)
    positions = self._get_positions(display,offsets)
    for icon,pos in zip(ICONS,positions):
      itext = Label(ifont,text=icon,color=0xFFFFFF,background_color=0x0000FF)
      itext.anchored_position = pos[0]
      itext.anchor_point = pos[1]
      self._group.append(itext)

  # --- query positions of icons   -------------------------------------------

  def _get_positions(self,display,offsets):
    """ return list of (position,anchorpoints) for all icons """

    positions = []
    for off in offsets:
      # fix relative offsets
      if 0 < abs(off[0]) < 1:
        xp = off[0]*display.width
      else:
        xp = off[0]
      if xp < 0:
        # right edge of the screen
        xp = display.width + xp; xa = 1
      else:
        xa = 0
      if 0 < abs(off[1]) < 1:
        yp = off[1]*display.height
      else:
        yp = off[1]
      if yp < 0:
        yp = display.height + yp
      positions.append(((xp,yp),(xa,0.5)))
    return positions

  # --- show logo or name   --------------------------------------------------

  def show(self,channel=None,img=None):
    """ load and show logo. Pass img to show explicit bmp (e.g. error) """

    if img:
      logo_path = f"/logos/{img}.bmp"
    else:
      logo_path = f"/logos/{channel.logo}.bmp"
    try:
      self._show_image(logo_path)
    except Exception as ex:
      print(f"logo {logo_path} not found (exception: {ex})")
      self._show_image(f"/logos/default.bmp")

  # --- show image   ---------------------------------------------------------

  def _show_image(self,path):
    """ load logo-image as TileGrid """

    if len(self._group) > 4:
      self._group.pop()
      gc.collect()

    f = open(path, "rb")
    pic = displayio.OnDiskBitmap(f)
    x = int((self._display.width-pic.width)/2)
    y = int((self._display.height-pic.height)/2)
    t = displayio.TileGrid(pic, x=x,y=y, pixel_shader=pic.pixel_shader)
    self._group.append(t)
    self._display.refresh()
