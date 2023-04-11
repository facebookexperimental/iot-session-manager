# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


# Generates private key using RSA algorithm
openssl genpkey -algorithm RSA \
                -pkeyopt rsa_keygen_bits:2048 \
                -outform pem \
                -out private_key.pem

# Uses private key to generate a RSA public key
openssl rsa -in private_key.pem -pubout -out public_key.pem

# Converts PEM from PKCS#8 to PKCS#1
openssl rsa -pubin -in public_key.pem -RSAPublicKey_out -out rsa_pub_key.pem

# Converts public key into the RSA Public Key format required for JWT Auth
openssl rsa -RSAPublicKey_in -in rsa_pub_key.pem  -inform PEM  -outform DER -RSAPublicKey_out  -out rsa_pub_key.der

# Copy der key to mqtt_broker config
cp ./rsa_pub_key.der ../../mqtt_broker/dev_jwt_auth/rsa_pub_key.der
