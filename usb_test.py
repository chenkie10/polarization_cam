import libusb
import usb.core
import usb.util
import sys
# idVendor=0x046D, idProduct=0xC05A
# find our device
dev = usb.core.find(idVendor=0x046D, idProduct=0xC05A)

# was it found?
if dev is None:
    raise ValueError('Device not found')

print(dev)
