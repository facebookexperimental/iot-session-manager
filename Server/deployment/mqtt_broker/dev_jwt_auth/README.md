# Configuration Required

Mosquitto JWT authentication utilizes an open source plugin and requires a third party binary found here:
https://github.com/wiomoc/mosquitto-jwt-auth

You can clone and build from source or download the prebuild release for linux and add it to this folder:
https://github.com/wiomoc/mosquitto-jwt-auth/releases/tag/0.4.0

The Dockerfile included assumes you are using the prebuilt linux release.
You will need to adjust the location of the binary in the mosquitto.conf accordingly.

If you want to build the plugin yourself you would need to create a Dockerfile that does that.
