To test the JWT authentication locally you must use dev-jwt-auth mode in the .env file in the deployment root folder and create and configure your private and public keys using openssl.

The `dev_rsa_keygen.sh` script runs the following commands to automate this.

NOTE: On windows, run `bash dev_rsa_keygen.sh` from a git bash terminal



1. Gen private key
openssl genpkey -algorithm RSA \
                -pkeyopt rsa_keygen_bits:4096 \
                -outform pem \
                -out private_key.pem


2. Generate public key from private key in PEM format
`openssl rsa -in private_key.pem -pubout -out public_key.pem`

3. Converts PEM from PKCS#8 to PKCS#1
`openssl rsa -pubin -in public_key.pem -RSAPublicKey_out -out rsa_pub_key.pem`

4. Convert public key to DER format for JWT Authentication
`openssl rsa -RSAPublicKey_in -in public_key.pem  -inform PEM  -outform DER -RSAPublicKey_out  -out public_key.der`


5. Move a copy of the public_key.der to the mqtt_broker/dev_jwt_auth folder
`cp ./public_key.der ../../mqtt_broker/dev_jwt_auth`
