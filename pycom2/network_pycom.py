#imports
import network
from network import WLAN

#this sets up the network access point with the following parameters
wlan = WLAN(mode=WLAN.AP, ssid = 'Pycom', auth =None, channel=1,antenna=None,power_save=False,hidden=True)
print("network setup")
