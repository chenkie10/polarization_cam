from arena_api import enums
from arena_api.buffer import BufferFactory
from arena_api.system import system
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk#图像控件
import time

def create_devices_with_tries():
    """
    This function waits for the user to connect a device before raising
    an exception
    """

    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    while tries < tries_max:  # Wait for device for 60 seconds
        devices = system.create_device()
        if not devices:
            print(
                f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
                f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1 } seconds passed ',
                      '.' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')
def configure_some_nodes(nodemap, stream_nodemap):

    # Enable stream auto negotiate packet size
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
    # Optional:
    # The pixel format can be checked to a void conversion if possible:
    # Code:
    '''
    if buffer.pixel_format == enums.PixelFormat.BGR8:
        return buffer
    '''
    print('Converting image buffer pixel format to BGR8 ')
    return BufferFactory.convert(buffer, enums.PixelFormat.BGR8)
#界面画布更新图像
# def tkImage():
#     ref,frame=cap.read()
#     frame = cv2.flip(frame, 1) #摄像头翻转
#     cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     pilImage=Image.fromarray(cvimage)
#     pilImage = pilImage.resize((image_width, image_height),Image.ANTIALIAS)
#     tkImage =  ImageTk.PhotoImage(image=pilImage)
#     return tkImage
def example_entry_point():
    devices = create_devices_with_tries()
    device = devices[0]
    print(f'Device used in the example:\n\t{device}')



    # print(f'Device used in the example:\n\t{device}')

#界面画布更新图像






if __name__ == '__main__':
    print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('\nExample started\n')
    example_entry_point()
    print('\nExample finished successfully')