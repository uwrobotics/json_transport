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
from std_msgs.msg import String


def pack(data):
    """
    Pack a Python object (e.g. dict or list) into a std_msgs.msg.String by converting it to a JSON string.
    """
    return String(data=json.dumps(data))


def unpack(message):
    """
    Unpack a std_msgs.msg.String into a Python object by loading from the JSON string.
    """
    return json.loads(message.data if message.data else "null")


class PackedJson(StringMsg):
    """
    A convenience class that wraps std_msgs.msg.String to store JSON data.
    Optionally validates the data against a JSON schema before storing.
    """

    def __init__(self, data=None, schema=None):
        super().__init__()
        if schema:
            validate(instance=data, schema=schema)
        # Store the JSON string in the 'data' field
        self.data = json.dumps(data) if data is not None else ""

    @property
    def json_data(self):
        """
        Get the JSON-parsed Python object from the stored JSON string.
        """
        return json.loads(self.data) if self.data else None

    @json_data.setter
    def json_data(self, value):
        """
        Set the JSON data by converting a Python object into a JSON string.
        """
        self.data = json.dumps(value)

    def __str__(self):
        return str(self.json_data)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.json_data)})"