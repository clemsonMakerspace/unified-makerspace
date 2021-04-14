#!/usr/bin/env bash
# stop script on error
set -e

# # Check to see if root CA file exists, download if not
# if [ ! -f ./root-CA.crt ]; then
#   printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
#   curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
# fi

# # Check to see if AWS Device SDK for Python exists, download if not
# if [ ! -d ./aws-iot-device-sdk-python ]; then
#   printf "\nCloning the AWS SDK...\n"
#   git clone https://github.com/aws/aws-iot-device-sdk-python.git
# fi

# # Check to see if AWS Device SDK for Python is already installed, install if not
# if ! python -c "import AWSIoTPythonSDK" &> /dev/null; then
#   printf "\nInstalling AWS SDK...\n"
#   pushd aws-iot-device-sdk-python
#   pip install AWSIoTPythonSDK
#   result=$?
#   popd
#   if [ $result -ne 0 ]; then
#     printf "\nERROR: Failed to install SDK.\n"
#     exit $result
#   fi
# fi

PRIVATE_KEY="../certs/XXXXXXXXXX-private.pem.key" # enter name of private key credential file
DEVICE_CERT="../certs/XXXXXXXXXX-certificate.pem.crt" # enter name of device credential file
DEVICE_NAME="CUmakeit_XX" # enter which number Pi system is being used
CA_CERT="../certs/root-CA.crt" 
THING_ENDPOINT="a5oyk3iuhy30n-ats.iot.us-east-1.amazonaws.com"
TOPIC="thing/makerspace_pi/signin"
PORT=8883
THING_NAME="CUmakeit_XX" # enter which number Pi system is being used
LOCATION="Watt_Center" # location Pi is in. NOTE THERE CANNOT BE A SPACE
EVENT="SignIn"
HAT_CONNECTED="True"

python signin.py --endpoint $THING_ENDPOINT --root-ca $CA_CERT --cert $DEVICE_CERT --key $PRIVATE_KEY --location $LOCATION --event $EVENT --topic $TOPIC --hat-connected $HAT_CONNECTED