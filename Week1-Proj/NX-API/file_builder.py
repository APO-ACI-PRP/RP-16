#!/usr/bin/env python

import csv
import sys
import json
import requests
import auto_vpc
import auto_vlan
import host_gen
import yaml
import collections
import ordereddict
import os

def build(var1,var2):

	vpc_info = var1

	vlan_info = var2

	try:
		n9k_dict = auto_vpc.sw_dict(vpc_info)
	except: # catch *all* exceptions
		raise
		sys.exit(1)

	try:
		vlan_dict = auto_vlan.vlan_dict(vlan_info)
	except: # catch *all* exceptions
		raise
		sys.exit(1)

	#-- GENERATE YAML FILES FOR SWITCHES IN DEVICE.CSV --#
	for switch in sorted(n9k_dict.keys()):

		global file_name

		file_name = "/etc/ansible/host_vars/" + switch + ".yml"

		with open(file_name, 'w') as outfile:
			outfile.write("--- \n")
			outfile.write( yaml.dump(n9k_dict[switch], default_flow_style=False))
			outfile.close()
			
			#-- SECTION TO BUILD VLAN LIST AND PORT-CHANNEL ALLOWD LIST--#
			with open(file_name, 'a') as outfile: 
			    outfile.write("vlans: \n")
			    for vlan in sorted(vlan_dict.keys()):
			    	list_member = " - {vlan_id: " + vlan_dict[vlan]['vlan_id'] + ", vlan_name: " + vlan_dict[vlan]['vlan_name'] + ', vlan: ' + vlan_dict[vlan]['vpc'] +"}\n"
			    	outfile.write(list_member)
	
			#-- SECTION TO BUILD VLAN ALLOWED STRING --#
			with open(file_name, 'a') as outfile:
				outfile.write("VPC_VLANS: '")
				last = vlan_dict.keys()[-1]

				vlan_list = ""
				for vlan in vlan_dict.keys():
					if vlan is vlan_dict.keys()[-1]:
						vlan_list = vlan_list + vlan_dict[vlan]['vlan_id'] +"'\n"
						outfile.write(vlan_list)
					else:
						vlan_list = vlan_list + vlan_dict[vlan]['vlan_id']+","

	outfile.close()

	host_gen.hostfile(n9k_dict)