# Software License Agreement (BSD)
#
# \file      json_transport.py
# \authors   Paul Bovbel <pbovbel@locusrobotics.com>, adapted for ROS 2
# \copyright Copyright (c) (2018,)
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#   ...
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.

import rclpy
import json
from jsonschema import validate, ValidationError

# If your package is called "json_msgs" and your message is named "Json.msg", 
# the generated Python module is typically accessible as below:
from json_msgs.msg import Json as JsonMsg


def pack(data):
    """
    Pack a Python dictionary/list/etc. into a JsonMsg by dumping to JSON.
    """
    return JsonMsg(json=json.dumps(data))


def unpack(message):
    """
    Unpack a JsonMsg into a Python object (dict, list, etc.) by loading from JSON.
    """
    return json.loads(message.json if message.json else "null")


class PackedJson(JsonMsg):
    """
    A convenience class that wraps the JsonMsg in a Python object.
    Optionally validates the data against a JSON schema before storing.
    """

    def __init__(self, data=None, schema=None):
        super().__init__()
        if schema:
            validate(instance=data, schema=schema)
        self.data = data  # Calls set_data() internally

    def set_data(self, data):
        self.json = json.dumps(data)

    def get_data(self):
        return json.loads(self.json)

    data = property(get_data, set_data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return "{name}({data})".format(name=self.__class__.__name__, data=repr(self.data))
