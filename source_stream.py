
import cv2
import time
from tkinter import *

# pip3 install numpy
import numpy as np
# pip3 install pillow
from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTk

from arena_api import enums
from arena_api.buffer import BufferFactory
from arena_api.system import system

def create_devices_with_tries():
    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    while tries < tries_max:  # Wait for device for 60 seconds
        devices = system.create_device()
        if not devices:
            print(
                f'Try {tries + 1} of {tries_max}: waiting for {sleep_time_secs} '
                f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1} seconds passed ',
                      '.' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')



def configure_some_nodes(nodemap, stream_nodemap):
    stream_nodemap['StreamAutoNegotiatePacketSize'].value = True

    # Enable stream packet resend
    stream_nodemap['StreamPacketResendEnable'].value = True

    # Width and height --------------------------------------------------------
    print('Getting \'Width\', \'Height\', and \'PixelFormat\' Nodes')
    nodes = nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    # Set width and height to their max values
    print('Setting \'Width\' and \'Height\' Nodes value to their '
          'max values')
    nodes['Width'].value = nodes['Width'].max
    nodes['Height'].value = nodes['Height'].max

    # Pixel format ------------------------------------------------------------
    new_pixel_format = 'Mono8'
    print(f'Setting \'PixelFormat\' to \'{new_pixel_format}\'')
    nodes['PixelFormat'].value = new_pixel_format
def convert_buffer_to_BGR8(buffer):
    print('Converting image buffer pixel format to BGR8 ')
    return BufferFactory.convert(buffer, enums.PixelFormat.BGR8)




device=system.create_device()
cap = cv2.VideoCapture('169.254.41.32')#创建摄像头对象

while True:
    ret,image=cap.read()
    cv2.imshow('test',image)

cv2.destroyAllWindows()

