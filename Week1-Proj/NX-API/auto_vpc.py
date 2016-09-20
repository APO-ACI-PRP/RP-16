#!/usr/bin/env python

import csv
import sys
import json
import requests
from collections import defaultdict

vpc_info_file = ""


def vpc_info(vpccsv):
	try:
		global vpc_info_file
		vpc_info_file = open(vpccsv)
	except IOError:
		print "ERROR UPLOADING VPC FILE"
		raise
		sys.exit(1)
	except IndexError:
		print "######################\nERROR: INCORRECT USAGE \n######################\nUsage: " + templates[0] + " <vpc config file> \n"
		raise
		sys.exit(1)

def sw_dict(csvfile):

	global vpc_info_file

	vpc_info(csvfile)

	while vpc_info_file:
		vpc_info_in = csv.DictReader(vpc_info_file)
		vpc_config = [line for line in vpc_info_in]

		#-- set default dictionary to allsw_dict to allow for adding --#
		allsw_dict = defaultdict(dict)

		#-- loop through CSV and create nested dictionary for each entry --#
		for sw_config in vpc_config:
			swname = sw_config['hostname']
			allsw_dict[swname]['mgmt_ip'] = sw_config['mgmt_ip']
			allsw_dict[swname]['hostname'] = sw_config['hostname']
			allsw_dict[swname]['username'] = sw_config['username']
			allsw_dict[swname]['password'] = sw_config['password']
			allsw_dict[swname]['vpc_domain'] = sw_config['vpc_domain']
			allsw_dict[swname]['KA_ip'] = sw_config['KA_ip']
			allsw_dict[swname]['PKA_ip'] = sw_config['PKA_ip']
			allsw_dict[swname]['KA_vlan'] = sw_config['KA_vlan']
			allsw_dict[swname]['vpc_rp'] = sw_config['vpc_rp']
			allsw_dict[swname]['peer_link'] = sw_config['pl_pc']
			allsw_dict[swname]['non_vpc_link'] = sw_config['nvpc_pc']
			allsw_dict[swname]['l3_link'] = sw_config['l3_pc']
			allsw_dict[swname]['l3_pc_ip'] = sw_config['l3_pc_ip']

		#-- FUNCTION RETURNS DICTIONARY CREATED ABOVE --#
		return allsw_dict

