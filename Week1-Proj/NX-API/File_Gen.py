#!/usr/bin/env python

import sys
import file_builder

csv_input = sys.argv

vpc_info = csv_input[1]
vlan_info = csv_input[2]

file_builder.build(vpc_info,vlan_info)


