# Initial imports
from __future__ import absolute_import
from __future__ import print_function

import pyshorteners
import mysql.connector
import datetime
import evdev
import subprocess
import argparse
import sys
import threading
import time
import qrcode
import json
import configparser
#import boto3
import requests

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from inky import InkyWHAT
from PIL import Image, ImageDraw
from mysql.connector import Error
from pyshorteners import Shorteners

############################################################################################
#                                                                                          #
#                                SOME INITIAL SETUP BELOW                                  #
#                                                                                          #
############################################################################################

'''
config = configparser.ConfigParser()
try:
    config.read_file(open('../../../config.ini'))
except(IOError):
    print("Could not find the configuration file. Please email moherol@g.clemson.edu to request the config file.")
'''
# Command-line arguments for the IoT connections.
parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")

# If you need to add more command line arguments to this function, add them here.
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                    "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--cert', help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                    "Necessary if MQTT server uses a certificate that's not already in " +
                                    "your trust store.")
parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
parser.add_argument('--topic', default="samples/test", help="Topic to subscribe to, and publish messages to.")
parser.add_argument('--location', default = "Default Location")
parser.add_argument('--event', default="Sign In")
parser.add_argument('--hat-connected', default="True")
args = parser.parse_args()

# Premade code from sample AWS starter code.
# ***DO NOT TOUCH unless you know what you are doing***
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

def scanCard():
    """Scans ID from a card reader attached to the Raspberry Pi.

    This function uses python-evdev to interface with the card
    scanner attached to the pi.

    Returns:
        The ID as an integer attached to the Card that was scanned.
        This is usually a 6-digit integer.
        For example: ID = 123456

        Returns -1 if there was an error finding a card scan device.
    """

    # Device should always be event0 unless more devices are plugged in.
    try:
        device = evdev.InputDevice('/dev/input/event0')
    except:
        print("Could not find a card scanner device attached.")
        return -1

    # Get input events (keystrokes) and append each input to the file.
    # The card scanner emulates a keyboard and therefore we need to parse
    # the input as keystrokes here.
    count = 0
    cardID = ""
    print("[Ready for a new scan]")
    for event in device.read_loop():
        # IDs should not be longer than 7 digits.
        if count == 7:
            break
        # This tests for keystrokes between 0-9 and writes it to the file.
        # See the python-evdev docs for more information.
        if (event.type == evdev.ecodes.EV_KEY and event.value == 1):
            if (event.code == 11):
                if (count >= 1):
                    cardID += str("0")
                count += 1
            elif(event.code >= 2 and event.code <= 10):
                cardID += (str(event.code - 1))
                count += 1
        # End of cardscanning
    print("Card ID found, ID: " + cardID)
    return int(cardID)

def connectToAWS(cardID):
    """Connects our device to AWS IoT in order to send information to AWS.

    We use AWS IoT to send messages from the device containing information
    like the card ID, time of scanning, location, etc. To get some of this
    external information like location, we pass them in with command-line
    arguments.
    """

    ############################################################################################
    #                                                                                          #
    #        BELOW IS CODE TO CONNECT TO THE IOT TOPIC AND SEND A MESSAGE TO THE TOPIC         #
    #                                                                                          #
    ############################################################################################

    print("Setting up AWS Connections...")

    # Establish an mqtt connection to publish and subscribe to topics on.
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        client_bootstrap=client_bootstrap, # Don't know what this is; don't touch it
        ca_filepath=args.root_ca,
        #on_connection_interrupted=on_connection_interrupted, # Don't know what this is; don't touch it
        #on_connection_resumed=on_connection_resumed, # Don't know what this is; don't touch it
        client_id=args.client_id,
        clean_session=False, # Don't know what this is; don't touch it
        keep_alive_secs=6) # Don't know what this is; don't touch it

    print("> Connecting to '{}' with client ID '{}'".format(args.endpoint, args.client_id))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available.
    connect_future.result()
    print("> Connected!")

    # Subscribe to the topic passed in from the arguments.
    print("> Subscribing to topic '{}'".format(args.topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=args.topic,
        qos=mqtt.QoS.AT_LEAST_ONCE)

    subscribe_result = subscribe_future.result()
    print("> Subscribed with {}".format(str(subscribe_result['qos'])))

    ############################################################################################
    #                                                                                          #
    #        BELOW IS WHAT SHOULD BE EDITED TO CHANGE WHAT MESSAGE IS SENT TO THE TOPIC        #
    #                                                                                          #
    ############################################################################################

    # Message JSON <<THIS IS WHAT GETS SENT TO THE TOPIC>>
    msg = {
    "ID": cardID,
    "Location": args.location,
    "Event": args.event,
    "DateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    message = json.dumps(msg)
    print("> Publishing message to topic '{}': {}".format(args.topic, message))
    mqtt_connection.publish(
        topic=args.topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    time.sleep(1)

    # Disconnect the connection after our message has been sent.
    disconnect_future = mqtt_connection.disconnect()
    print("Disconnecting from AWS...")
    disconnect_future.result()

# def changeScreens(cardID):
#     """Changes the screen shown on the Raspberry Pi Hat.
#
#     Checks to see if the card is in the database and displays
#     the corresponding screen.
#
#     We are using the inkywHAT Red/Black/White:
#     https://shop.pimoroni.com/products/inky-what?variant=13590497624147
#
#     Documentation:
#     https://github.com/pimoroni/inky
#
#     TODO: Change the screen back to "please scan card" after a set amount of time has passed.
#     Needs some multithreading or something to accomplish that I think.
#     """
#
#     ######## Pi Hat Setup ########
#     print("Changing screens...")
#
#     inkywhat = InkyWHAT('black')
#
#     # Establish a new connection for checking if the card is in the DB.
#     # Not sure if this is required, but this is the easiest way I could find to do it.
#     # Copy-pasted from the earlier mqtt_connection variable.
#     pi_hat_connection = mqtt_connection_builder.mtls_from_path(
#         endpoint=args.endpoint,
#         cert_filepath=args.cert,
#         pri_key_filepath=args.key,
#         client_bootstrap=client_bootstrap,
#         ca_filepath=args.root_ca,
#         client_id=args.client_id,
#         clean_session=False,
#         keep_alive_secs=6)
#
#     # Query the DB to see if that card is in it.
#     # Use the config defined at the top of the file to hide connection information.
#     cardInDBResult = False
#     lambda_url = "https://td6vp4rpi5.execute-api.us-east-1.amazonaws.com/prod/SignIn"
#     lambda_payload = {"HardwareID":cardID, "LoginLocation": args.location}
#     try:
#         response = requests.post(lambda_url, data = lambda_payload)
#         mysqlConn = mysql.connector.connect(host="makerdata.cmas8ftjsupb.us-east-1.rds.amazonaws.com",
#                                             database="makerdata",
#                                             user="admin",
#                                             password="20Maker;20Data$")
#         if mysqlConn.is_connected():
#             print("Connected to database...")
#             cursor = mysqlConn.cursor()
#             cursor.execute("select database();")
#             record = cursor.fetchone()
#             lookForCardQuery = "SELECT * FROM Student_ID WHERE SID = " + str(cardID)
#             cursor.execute(lookForCardQuery)
#             records = cursor.fetchall()
#             if(cursor.rowcount > 0):
#                 cardInDBResult = True
#     except Error as e:
#         print("Error while connecting to MySQL Database", e)
#     finally:
#         if (mysqlConn.is_connected()):
#             cursor.close()
#             mysqlConn.close()
#             print("Disconnected from database...")
#
#     # If the card is in the database, set the screen to be shown to the "Welcome" screen
#     if (cardInDBResult):
#         print("ID Found - Displaying Welcome...")
#         imgURL = "../../../qrcode/displayScreens/welcome_bw.png"
#         im = Image.open(imgURL)
#
#         # Resizing the image so it fits to the screen
#         # This is specific to the inkywhat, otherwise it claims that there is a size-mismatch.
#         size = (400,300)
#         out = im.resize(size)
#         out.save('../../../qrcode/resize-output.png')
#         img = Image.open('../../../qrcode/resize-output.png')
#         pal_img = Image.new("P", (1, 1))
#         pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
#         img = img.convert("RGB").quantize(palette=pal_img)
#
#     # If the card is not in the database, make a QR code and show the "QR Code" screen
#     elif (not cardInDBResult):
#         print("ID Not Found - Displaying Registration...")
#         imgURL = "../../../qrcode/displayScreens/qrscan_bw.png"
#         displayURL = "../../../qrcode/qrCodeScreenMerged.png"
#
#         # Generate a QR Code Object
#         qr = qrcode.QRCode(
#             version=None,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=3,
#             border=2,
#         )
#
#         # Generate the URL the code points to and add it to the QR Code
#         wURL = "https://makerspace-registration.s3.amazonaws.com/index.html?id=" + str(cardID)
#         qr.add_data(wURL)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#
#         # Save the generated QR Code to the proper tests
#         img.save('../../../qrcode/qr_image.png')
#         im = Image.open(imgURL)
#
#         # Resizing the image so it fits to the screen
#         size = (400,300)
#         out = im.resize(size)
#         out.save('../../../qrcode/resize-output.png')
#
#         # We are using ImageMagick installed on the Raspberry Pi to
#         # composite our generated QR Code onto the premade image
#         # with this subprocess call. This could be changed to a
#         # bash script called in the same way.
#         s = pyshorteners.Shortener(Shorteners.TINYURL)
#         shortLink = s.short(wURL)
#         composeQRCodeOntoImageCommand = 'composite -blend 100 -gravity center ../../../qrcode/qr_image.png ../../../qrcode/resize-output.png ../../../qrcode/qrCodeScreenMerged.png'
#         composeShortLinkOntoImageCommand = 'convert ../../../qrcode/qrCodeScreenMerged.png -font Arial -gravity North -pointsize 24 -annotate +0+215 \'' + shortLink + '\' ../../../qrcode/qrCodeScreenMerged.png'
#         subprocess.call(composeQRCodeOntoImageCommand, shell=True)
#         subprocess.call(composeShortLinkOntoImageCommand, shell=True)
#
#         img = Image.open(displayURL)
#
#         # Continue resizing, inkywhat complains otherwise.
#         pal_img = Image.new("P", (1, 1))
#         pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
#         img = img.convert("RGB").quantize(palette=pal_img)
#
#     # Update the image on the screen and show it.
#     inkywhat.set_image(img)
#     inkywhat.set_border('white')
#     inkywhat.show()
#     print("Finished changing screens...")

def callLambda(cardID):
    # Establish a new connection for checking if the card is in the DB.
    # Not sure if this is required, but this is the easiest way I could find to do it.
    # Copy-pasted from the earlier mqtt_connection variable.
    pi_hat_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        client_bootstrap=client_bootstrap,
        ca_filepath=args.root_ca,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=6)

    # Query the DB to see if that card is in it.
    # Use the config defined at the top of the file to hide connection information.
    cardInDBResult = False
    lambda_url = "https://7becb2gddl.execute-api.us-east-1.amazonaws.com/iot/signout"
    lambda_payload = {"HardwareID":str(cardID)}
    try:
	print("payload is " + str(lambda_payload))
        response = requests.post(lambda_url, json = lambda_payload)
        cardInDBResult = True
        print("This should have worked "+ str(response.text))
    except requests.exceptions.RequestException as e:
        print(str(e))
	print("this didn't work")
        cardInDBResult = False

# Main body loop
while(True):
    # Called when a card is scanned.
    # Sets the scanned ID to cardID.
    cardID = scanCard()
    connectToAWS(cardID)
    if (args.hat_connected == "True"):
	print("starting to check if cardID is in DB")
	#changeScreens(cardID)
    callLambda(cardID)
    print("CardID is :" + str(cardID))
