# ----------------------------------------------------------------------------
# settings_template.py: Network, hardware and application configuration
#                       (blueprint file). Copy this file to settings.py.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/cp-webradio
#
# ----------------------------------------------------------------------------

class Settings:
  pass

# network configuration   ----------------------------------------------------

secrets  = Settings()
secrets.ssid      = 'my_ssid'
secrets.password  = 'my_secret_pasword'
secrets.retries   = 3
secrets.timeout   = 10

# hardware configuration   ---------------------------------------------------

from hw_config_display_audio_pack import hw_config

# app configuration   --------------------------------------------------------

app_config = Settings()
app_config.debug = True
app_config.bufsize = 16384
app_config.max_wait = 10                         # for channel to start playing
app_config.switch_delay = 1                      # delay playing after switch

#app_config.autoplay = "BR Klassik"              # autoplay after boot

# favorite channels for extra buttons, see hw_config_waveshare_13.py
# on how to use this
#app_config.favorites = ["BR Klassik", "MDR KLASSIK"]
