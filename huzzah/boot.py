#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()

#this huzzah has a boot.py function, so all commands will run on boot
#runs the network setup
import network_huzzah
