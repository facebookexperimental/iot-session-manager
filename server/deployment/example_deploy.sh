#!/bin/bash

# Download code onto instance (can be done from S3 bucket to simplify startup for ASG)
<Github or other code to download files into folder without overwriting config >
# Example from S3

# This assums that the necessary configuration files (certs) have been provisioned in iot-session-manager/config
# Copy configuration files (certs, keys, etc) into the location for docker compose to user
cp /iot-session-manager/config/server.crt /iot-session-manager/server/deployment/certs/prod_ssl/server.crt
cp /iot-session-manager/config/server.key /iot-session-manager/server/deployment/certs/prod_ssl/server.key

# The mqtt_pub_key_info.json file is the output of KMS get-public-key command that can be run to download the file into config
cp /iot-session-manager/config/mqtt_pub_key_info.json /iot-session-manager/server/deployment/mqtt_broker/kms_jwt_auth/mqtt_pub_key_info.json
cp /iot-session-manager/config/mqtt_pub_key_info.json /iot-session-manager/server/session_manager/mqtt_pub_key_info.json


# Write variables to .env file for docker compose setup
cd /iot-session-manager/server/deployment/
cat <<EOF > .env
deployment_mode=prod
mqtt_auth_mode=kms_jwt_auth
aws_region=us-west-2
EOF

# Run the key conversion script which converts public key from PKCS #8 to #1 format
cd /iot-session-manager/server/deployment/mqtt_broker/kms_jwt_auth
python3 kms_pub_convert.py

#Convert pub_key #1 format from PEM to DER
openssl rsa -RSAPublicKey_in -in rsa_pub_key.pem  -inform PEM  -outform DER -RSAPublicKey_out  -out rsa_pub_key.der

# Navigate to main deployment foler and rebuild docker compose
cd /iot-session-manager/server/deployment
docker compose down
docker compose build
docker compose up -d
