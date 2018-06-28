#imports
import network
from network import WLAN

#this sets up the network access point with the following parameters
ap_if = network.WLAN(mode=network.WLAN.STA_AP, ssid = 'Pycom', auth =None, channel=1,power_save=False,hidden=True)
ap_if.init(mode=network.WLAN.STA_AP, ssid = 'Pycom', auth =None, channel=1,power_save=False,hidden=True)
print("network setup")
