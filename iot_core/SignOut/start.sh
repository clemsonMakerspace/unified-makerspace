#!/usr/bin/env bash
# stop script on error
set -e

# Check to see if root CA file exists, download if not
if [ ! -f ../certs/root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

PRIVATE_KEY="../certs/PrivateKeyCUmakeit_XX.pem.key" # enter name of private key credential file
DEVICE_CERT="../certs/CertificateCUmakeit_XX.pem.crt" # enter name of device credential file
DEVICE_NAME="CUmakeit_XX" # enter which number Pi system is being used
CA_CERT="../certs/root-CA.crt"
THING_ENDPOINT="a1gohrbna3djed-ats.iot.us-east-1.amazonaws.com"
TOPIC="thing/makerspace_pi/signout"
PORT=8883
THING_NAME="CUmakeit_XX" # enter which number Pi system is being used
LOCATION="    " # location Pi is in. NOTE THERE CANNOT BE A SPACE
EVENT="SignOut"
HAT_CONNECTED="True"

python signout.py --endpoint $THING_ENDPOINT --root-ca $CA_CERT --cert $DEVICE_CERT --key $PRIVATE_KEY --location $LOCATION --event $EVENT --topic $TOPIC --hat-connected $HAT_CONNECTED
