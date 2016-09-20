import requests
import json
import sys
import csv
import auto_vpc
from collections import defaultdict

url='http://172.31.217.135/ins'
switchuser='admin'
switchpassword='cisco123'

config = sys.argv

cfg_dir = "/home/cisco/Project/configs/"

device_info = config[1]

sw_list = auto_vpc.sw_dict(device_info)

push_to = defaultdict(dict)

for switch in sorted(sw_list.keys())

	vpc_cfg_in = push_to[switch]['hostname']+"-VPCcfg"

	with open(vpc_cfg_in, 'r') as cfgfile:
		vpc_cfg = cfgfile.read().replace('\n',' ;')

	#with open(config[2], 'r') as cfgfile:
		#mgmt_cfg = cfgfile.read().replace('\n',' ;')

	#with open(config[3], 'r') as cfgfile:
		#l3pc_cfg = cfgfile.read().replace('\n',' ;')

	#with open(config[4], 'r') as cfgfile:
		#FandV_cfg = cfgfile.read().replace('\n',' ;')

	vpc_cfg = "config t ;"+vpc_cfg
	mgmt_cfg = "config t ;"+mgmt_cfg
	l3pc_cfg = "config t ;"+l3pc_cfg
	FandV_cfg = "config t ;"+FandV_cfg

	#-- POST VPC CONFIGURATION --#
	myheaders={'content-type':'application/json'}
	payload={
	  "ins_api": {
	    "version": "1.0",
	    "type": "cli_conf",
	    "chunk": "0",
	    "sid": "1",
	    "input": vpc_cfg,
	    "output_format": "json"
	  }
	}
	vpc = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
	vpc_response = json.dumps(vpc,indent=4)
	print vpc_response

	#--- POST MANAGEMENT CONFIGURATION --#
	myheaders={'content-type':'application/json'}
	payload={
	  "ins_api": {
	    "version": "1.0",
	    "type": "cli_conf",
	    "chunk": "0",
	    "sid": "1",
	    "input": mgmt_cfg,
	    "output_format": "json"
	  }
	}
	mgmt = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
	mgmt_response = json.dumps(mgmt,indent=4)
	print mgmt_response

	#-- POST L3 CONFIGURATION --#
	myheaders={'content-type':'application/json'}
	payload={
	  "ins_api": {
	    "version": "1.0",
	    "type": "cli_conf",
	    "chunk": "0",
	    "sid": "1",
	    "input": l3pc_cfg,
	    "output_format": "json"
	  }
	}
	print l3pc_cfg
	l3pc = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
	l3pc_response = json.dumps(l3pc,indent=4)
	print mgmt_response

	#-- POST VLAN INFORMATION --#
	myheaders={'content-type':'application/json'}
	payload={
	  "ins_api": {
	    "version": "1.0",
	    "type": "cli_conf",
	    "chunk": "0",
	    "sid": "1",
	    "input": FandV_cfg,
	    "output_format": "json"
	  }
	}
	print FandV_cfg
	FandV = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
	FandV_response = json.dumps(FandV,indent=4)
	print FandV_response