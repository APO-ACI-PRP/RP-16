#!/usr/bin/env python

import csv
import sys
import json
import requests
from collections import defaultdict

vlan_info_file = ""

def vlan_info(vlancsv):
	try:

		global vlan_info_file

		vlan_info_file = open(vlancsv)
		#print "VLAN Config Upload Successful"
	except IOError:
		print "ERROR UPLOADING VLAN FILE"
		raise
		sys.exit(1)
	#print VLAN_info_file
	except IndexError:
		print "######################\nERROR: INCORRECT USAGE \n######################\nUsage: " + templates[0] + " <vlan config file> \n"
		raise
		sys.exit(1)

def vlan_dict(csvfile):

	global vlan_info_file

	vlan_info(csvfile)

	#print vlan_info
	while vlan_info_file:
		vlan_info_in = csv.DictReader(vlan_info_file)
		vlan_config = [line for line in vlan_info_in]

		#print vlan_config

		#set default dictionary to allsw_dict to allow for adding 
		vlan_dict = defaultdict(dict)

		#loop through CSV and create nested dictionary for each entry
		for vlans in vlan_config:
			vlan = vlans['vlan_name']
			vlan_dict[vlan]['vlan_id'] = vlans['vlan_id']
			vlan_dict[vlan]['vlan_name'] = vlans['vlan_name']
			vlan_dict[vlan]['vpc'] = vlans['vpc']
		#return vlan dictionary created above
		#print vlan_config

		return vlan_dict
