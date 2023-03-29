# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

'''
This script is used for systems deployed on AWS where KMS is used to store a private key
for the JWT signing.
The `aws kms get-public-key` call provides the data in a JSON file with in the PKCS #8 format without headers,
The MQTT JWT Auth plugin for the broker needs a public key in the PKCS #1 format, which includes a subset of the #8 data with different headers.
More background info on #1 vs #8 format here:  https://stackoverflow.com/questions/18039401/how-can-i-transform-between-the-two-styles-of-public-key-format-one-begin-rsa

'''

import json

# The mqtt_pub_key_info.json file should be the result of the `aws kms get_public_key` command run from the instance
with open('mqtt_pub_key_info.json', 'rb') as pubdata:
    public_key_data = pubdata.read()

pub_dict = json.loads(public_key_data)

pubkey_string = pub_dict["PublicKey"]

'''
Data conversion from PKCS #8 to #1.

Given that AWS provides PKCS #8 data without the headers we can either:
1. Add headers, create a PKCS #8 file, and use OpenSSL to convert the file from #8 to # 1
OR
2. Remove the first 32 characters of the data string (converting from #8 to #1) and then add the headers.

Option 2 is a simpler solution so is seen below.
'''

pkcs1_string = pubkey_string[32:]
rsa_key = '-----BEGIN RSA PUBLIC KEY-----' + pkcs1_string +'-----END RSA PUBLIC KEY-----'
print(rsa_key)
with open("rsa_pub_key.pem", "w") as outfile:
    outfile.write(rsa_key)
