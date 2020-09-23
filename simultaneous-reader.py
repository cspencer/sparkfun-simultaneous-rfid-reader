#!/usr/bin/env python3

import mercury
import time

# DEVICE = "/dev/ttyUSB0"    # The location from which we'll be reading data
                             # when using a serial-to-usb convertor.  This may
                             # vary depending on the version of Raspbian or
                             # Raspberry Pi OS you are running.

DEVICE = "/dev/serial0"      # The location from which we'll be reading data
                             # when using the Pi's RX/TX GPIO pins.  This may
                             # vary depending on the version of Raspbian or
                             # Raspberry Pi OS you are running.


REGION = "NA2"               # The Region of Operation we'll use for the device.
                             # The full list of supported regions can be
                             # obtained with a call to the get_supported_regions
                             # method.

ANTENNAS = [1]               # A list of antennas that we'll be reading from to
                             # detect RFID tags.  The full list of available
                             # antennas can be obtained with a call to the
                             # get_antennas method.

PROTOCOL = "GEN2"            # The protocol that we'll be using to look for tags.
                             # The full list of protocol's is available in the
                             # documentation for the set_read_plan method.


def found_tag(data):
    print("Found a tag: " + str(data.epc))
    print("  Signal strength = " + str(data.rssi))
                             
def main():
    connected = False
    
    # Attempt to establish a connection to the reader.  Occasionally, the reader
    # fails to connect on the first try, at which point the merucy API will
    # throw a TypeError indicating the reader timed out.  If we catch a
    # TypeError, we'll sleep for a second and try again until it connects.
    while not connected:
        try:
            print("Connecting to Simultaneous RFID Reader on device: {}".format(DEVICE))
            reader = mercury.Reader("tmr://{}".format(DEVICE))
            connected = True
            print("Connected.")
        
        except TypeError as e:
            print("Got a TypeError exception: {}, retrying in 1 second".format(e))
            time.sleep(1)

    # Set the Region of Operation for the RFID reader to the 
    reader.set_region("NA2")

    # Create a read plan for the protocol and the antennas we'll be using.
    reader.set_read_plan(ANTENNAS, PROTOCOL)

    # We're going to be doing continuous asynchronous reads, so setup the
    # callback to be used when a tag is found.
    reader.start_reading(found_tag, on_time=250, off_time=250)

    # Keep looking for tags until we get a Ctrl-C, then exit.
    print("Looking for RFID tags; Press Ctrl-C to exit")
    try:
        while 1:
            print("Waiting for an RFID tag...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ctrl-C pressed; Shutting down RFID reader.")

    # Shutdown the reader and antenna.
    reader.stop_reading()

    print("Done.")
    
if __name__ == "__main__":
    main()
