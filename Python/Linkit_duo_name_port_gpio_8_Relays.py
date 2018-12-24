""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
#import RPi.GPIO as GPIO ## Import GPIO library
import serial
import mraa

from debounce_handler import debounce_handler

srl = serial.Serial("/dev/ttyS0", 57600)

logging.basicConfig(level=logging.DEBUG)

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"office": 52000}
    TRIGGERS = {"kitchen": 52000, "living room": 51000, "office": 53000, "room": 52002, "tv": 52003, "pc": 52004,
                "xbox": 52005, "light": 52006}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)

        ############# Switch state to revers the relay polarity ############
        if state==True:
         state = 1
        else:
         state = 0
        ############# Switch state to revers the relay polarity ############

        if name=="kitchen": #Controll MPU GPIO
            print("Kitch lights command send to MPU!")
            pin = mraa.Gpio(44)
            pin.dir(mraa.DIR_OUT)
            pin.write(state)
        elif name =="office": # Send command to MCU
            print("Office lights command send to MCU!")
            srl.write('{"device-name":"' + name + '","gpio":9,"state":' + str(state) + '}')
        elif name =="living room":
            print("living room lights command send to MCU!")
            srl.write('{"device-name":"' + name + '","gpio":14,"state":' + str(state) + '}')
        elif name == "room":
            print("Please implement device!")
        elif name == "tv":
            print("Please implement device!")
        elif name == "pc":
            print("Please implement device!")
        elif name == "xbox":
            print("Please implement device!")
        elif name == "light":
            print("Please implement device!")
        else:
            print("Please implement device!")




        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ str(e.args)  )
            break
