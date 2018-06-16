import network
from network import WLAN

wlan = WLAN(mode=WLAN.AP, ssid = 'Pycom', auth =None, channel=1,antenna=None,power_save=False,hidden=True)
print("network setup")
