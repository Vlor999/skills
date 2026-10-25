# fastscan.py - a fast scanner
# Copyright (C) 2019 Jordan Lee
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import re

_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+")


def scan(text):
    return _TOKEN.findall(text)
