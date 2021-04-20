#!/usr/bin/env bash
# stop script on error
set -e

Check to see if root CA file exists, download if not
if [ ! -f ../certs/root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

PRIVATE_KEY="../certs/XXXXXXXXXX-private.pem.key" # enter name of private key credential file
DEVICE_CERT="../certs/XXXXXXXXXX-certificate.pem.crt"
DEVICE_NAME="CUmakeit_01"
CA_CERT="../certs/root-CA.crt"
THING_ENDPOINT="a5oyk3iuhy30n-ats.iot.us-east-1.amazonaws.com"
TOPIC="thing/makerspace_pi/signout"
PORT=8883
THING_NAME="CUmakeit_01"
LOCATION="Watt_Center"
EVENT="SignOut"
HAT_CONNECTED="True"

# run pub/sub sample app using certificates downloaded in package
#printf "\nRunning pub/sub sample application...\n"
#python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e a5oyk3iuhy30n-ats.iot.us-east-1.amazonaws.com -r root-CA.crt -c CUmakeit_01.cert.pem -k CUmakeit_01.private.key

python signout.py --endpoint $THING_ENDPOINT --root-ca $CA_CERT --cert $DEVICE_CERT --key $PRIVATE_KEY --location $LOCATION --event $EVENT --topic $TOPIC --hat-connected $HAT_CONNECTED
