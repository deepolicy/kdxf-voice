#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jan. 1, 2019 -- inksci.com
Support: http://inksci.com/inkvoice
"""

from __future__ import print_function

import base64

# [INFO] [1546326105.567101]: /ink_control_19342_1546326060531I heard data: "5rC05p6c5Y+v5Lul5aSa5ZCD54K55ZOm44CC"
# ('data: ', 'u\xabZ\xe6\xb0\xb4\xe6\x9e\x9c\xe5\x8f\xaf\xe4\xbb\xa5\xe5\xa4\x9a\xe5\x90\x83\xe7\x82\xb9\xe5\x93\xa6\xe3\x80\x82')

data = "5rC05p6c5Y+v5Lul5aSa5ZCD54K55ZOm44CC"

data_2 = base64.b64decode( data )

print( "data_2: ", data_2 )
# data_2:  水果可以多吃点哦。