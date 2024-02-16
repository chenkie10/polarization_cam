# -----------------------------------------------------------------------------
# Copyright (c) 2022, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

from arena_api.system import system
from arena_api.buffer import *
from PIL import Image as PIL_Image
import ctypes
import numpy as np
import cv2
import time

'''
Live Stream: Introduction
    This example introduces the basics of running a live stream 
    from a single device. This includes creating a device, selecting
    up stream dimensions, getting buffer cpointer data, creating an
    array of the data and reshaping it to fit image dimensions using
    NumPy and displaying using OpenCV-Python.
'''


def create_devices_with_tries():
    '''
    This function waits for the user to connect a device before raising
        an exception
    '''

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


def setup(device):
    """
    Setup stream dimensions and stream nodemap
        num_channels changes based on the PixelFormat
        Mono 8 would has 1 channel, RGB8 has 3 channels

    """
    nodemap = device.nodemap
    nodes = nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    nodes['Width'].value = 2448
    nodes['Height'].value = 2048
    nodes['PixelFormat'].value = 'PolarizedAolp_Mono8'

    num_channels = 3

    # Stream nodemap
    tl_stream_nodemap = device.tl_stream_nodemap

    tl_stream_nodemap["StreamBufferHandlingMode"].value = "NewestOnly"
    tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True
    tl_stream_nodemap['StreamPacketResendEnable'].value = True

    return num_channels


def scale_linear_bycolumn(rawpoints, high=255.0, low=0.0):
    '''
    Scale the rawpoints array so that each "column" is
        normalized to the same scale Linear stretch from lowest value = 0 to
        highest value = 255 more :
        https://gist.github.com/perrygeo/4512375gistcomment-967246
    '''

    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)


def example_entry_point():
    """
    demonstrates live stream
    (1) Start device stream
    (2) Get a buffer and create a copy
    (3) Requeue the buffer
    (4) Calculate bytes per pixel for reshaping
    (5) Create array from buffer cpointer data
    (6) Create a NumPy array with the image shape
    (7) Display the NumPy array using OpenCV
    (8) When Esc is pressed, stop stream and destroy OpenCV windows
    """

    devices = create_devices_with_tries()
    device = devices[0]

    # Setup
    num_channels = setup(device)
    global prev_frame_time
    prev_frame_time = 0


    with device.start_stream():
        """
        Infinitely fetch and display buffer data until esc is pressed
        """
        while True:

            # Used to display FPS on stream

            buffer = device.get_buffer()
            item = BufferFactory.copy(buffer)
            device.requeue_buffer(buffer)
            buffer_bytes_per_pixel = int(len(item.data) / (item.width * item.height))

            def origin_img():

                """
                Buffer data as cpointers can be accessed using buffer.pbytes
                """
                array = (ctypes.c_ubyte * num_channels * item.width * item.height).from_address(
                    ctypes.addressof(item.pbytes))
                """
                Create a reshaped NumPy array to display using OpenCV
                """
                npndarray = np.ndarray(buffer=array, dtype=np.uint8,
                                       shape=(item.height, item.width, buffer_bytes_per_pixel))
                return npndarray

            def converting_hsv():
                scaled_nparray_reshaped = scale_linear_bycolumn(origin_img())
                scaled_nparray_reshaped_8 = np.uint8(scaled_nparray_reshaped)
                npndarray_hsv = cv2.applyColorMap(
                    scaled_nparray_reshaped_8, cv2.COLORMAP_HSV)
                #print('---------converting--------')
                return npndarray_hsv

            def snap_shot():
                time_now = time.time()
                cv2.imshow('snapshot' + format(time_now), converting_hsv())
                print('Saving image')
                png_name = f'from_Aolp_to_png_with_pil' + format(time_now) + '.png'
                cv2.imwrite(png_name,converting_hsv())
                return None

            def img_show(name, feature):
                global prev_frame_time
                curr_frame_time=time.time()
                fps = 1 / (curr_frame_time - prev_frame_time)
                prev_frame_time = curr_frame_time
                cv2.putText(feature, text="FPS:" + str(int(fps)), org=(0, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                            fontScale=1.0, color=(0, 0, 0))


                cv2.imshow(name, feature)
                return None

            key = cv2.waitKey(1)
            feature = converting_hsv()
            if key == 27:
                break
            if key == 32:
                snap_shot()
            img_show('Aolp_Mono8_HSV', feature)

            # BufferFactory.destroy(item)
            # if key == 27:
            #     break

    device.stop_stream()
    cv2.destroyAllWindows()

    system.destroy_device()


if __name__ == '__main__':
    print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('\nExample started\n')
    example_entry_point()
    print('\nExample finished successfully')
