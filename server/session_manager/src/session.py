# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from settings import CONDUCTOR_INTERFACES

'''
Session model that provides the data structure and methods for a given session.
'''


class Session():
    def __init__(self, id, pin, session_type):
        self.id = id
        self.pin = pin
        self.type = session_type
        self.clients = []
        self.conductor = CONDUCTOR_INTERFACES[session_type](self)

    def encode(self):
        return {"id":self.id, "pin":self.pin,"type":self.type,"clients":self.clients}

    def conductor_request(self, method, params):
        return self.conductor.request(method, params)
