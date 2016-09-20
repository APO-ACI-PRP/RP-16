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

csv_input = sys.argv

#vpc_info = csv_input[1]
#vlan_info = csv_input[2]

def yaml_build(vpc_info,vlan_info):
	try:
		n9k_dict = auto_vpc.sw_dict(vpc_info)
	except: # catch *all* exceptions
		sys.exit(1)

	try:
		vlan_dict = auto_vlan.vlan_dict(vlan_info)
	except: # catch *all* exceptions
		sys.exit(1)

	#print vlan_dict.keys()[-1]

	#generate YAML FILES FOR SWITCHES IN DEVICE CSV
	for switch in sorted(n9k_dict.keys()):

		global file_name

		file_name = switch + ".yml"

		with open(file_name, 'w') as outfile:
			outfile.write("--- \n")
			outfile.write( yaml.dump(n9k_dict[switch], default_flow_style=False))
			outfile.close()
			#-- SECTION TO BUILD VLAN LIST AND PORT-CHANNEL ALLOWD LIST--#

			with open(file_name, 'a') as outfile: 
			    outfile.write("vlans: \n")
			    for vlan in sorted(vlan_dict.keys()):
			    	list_member = " - { vlan_id: " + vlan_dict[vlan]['vlan_id'] + ", vlan_name: " + vlan_dict[vlan]['vlan_name'] + ', vlan: ' + vlan_dict[vlan]['vpc'] +"}\n"
			    	outfile.write(list_member)

	#print vlan_dict.keys()		

			with open(file_name, 'a') as outfile:
				outfile.write("VPC_VLANS: '")
				last = vlan_dict.keys()[-1]
				#print last	
				vlan_list = ""
				for vlan in vlan_dict.keys():
					if vlan is vlan_dict.keys()[-1]:
						vlan_list = vlan_list + vlan_dict[vlan]['vlan_id']
						outfile.write(vlan_list)
					else:
						vlan_list = vlan_list + vlan_dict[vlan]['vlan_id']+","
					
				outfile.write("'")
	outfile.close()