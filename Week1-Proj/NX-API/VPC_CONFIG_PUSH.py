import requests
import json
import sys
import csv
from StringIO import StringIO
import auto_vpc
from collections import defaultdict
import colors

config = sys.argv

cfg_dir = "/home/cisco/Project/configs/"

cfg_status = 0

device_info = config[1]

sw_list = auto_vpc.sw_dict(device_info)

def err_msg(dict,filename):

	for status in dict['ins_api']['outputs']['output']:

		if status['msg'] != 'Success':

			errtxt = filename+"-err.txt"
			with open(errtxt, 'w') as errfile:
				errfile.write(json.dumps(status,indent=4))
			errfile.close()

			return str("   - " + status['msg'] + " check "+errtxt+" for more information")

def config_status(resp,filename):
	global cfg_status
	cfg_status = 0

	for status in resp['ins_api']['outputs']['output']:
		if status['msg'] == 'Success':
			cfg_status = cfg_status+0
		else:
			cfg_status = cfg_status+1

	if cfg_status is 0:

		return str(colors.infog("Success"))
	else:
		return str(colors.err("Error: \n") + err_msg(resp,filename))


def nx_staging():
	global cfg_status

	for switch in sorted(sw_list.keys()):

		vpc_cfg = ""
		mgmt_cfg = ""
		l3pc_cfg = ""
		FandV_cfg = ""

		#-- POST INFORMATION --#
		url='http://'+sw_list[switch]['mgmt_ip']+'/ins'
		switchuser=sw_list[switch]['username']
		switchpassword=sw_list[switch]['password']

		#-- CONFIG LOCATIONS --#
		vpc_cfg_in = cfg_dir+sw_list[switch]['hostname']+"-VPC.cfg"
		mgmt_cfg_in = cfg_dir+sw_list[switch]['hostname']+"-MGMT.cfg"
		l3pc_cfg_in = cfg_dir+sw_list[switch]['hostname']+"-L3PC.cfg"
		FandV_cfg_in = cfg_dir+sw_list[switch]['hostname']+"-FandV.cfg"

		#-- READ IN VPC CONFIG FILE TO PUSH via POST --#
		with open(vpc_cfg_in, 'r') as cfgfile:
			vpc_cfg = cfgfile.read().replace('\n',' ;')

		vpc_cfg = "config t ;"+vpc_cfg

		#-- READ IN MGMT CONFIG FILE TO PUSH via POST --#
		with open(mgmt_cfg_in, 'r') as cfgfile:
			mgmt_cfg = cfgfile.read().replace('\n',' ;')

		mgmt_cfg = "config t ;"+mgmt_cfg

		#-- READ IN L3PC CONFIG FILE TO PUSH via POST --#
		with open(l3pc_cfg_in, 'r') as cfgfile:
			l3pc_cfg = cfgfile.read().replace('\n',' ;')

		l3pc_cfg = "config t ;"+l3pc_cfg

		#-- READ IN VPC CONFIG FILE TO PUSH via POST --#
		with open(FandV_cfg_in, 'r') as cfgfile:
			FandV_cfg = cfgfile.read().replace('\n',' ;')

		FandV_cfg = "config t ;"+FandV_cfg

		print colors.info('[INFO]') +' BEGIN CONFIGURATION PUSH TO ' + switch
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
		FandV = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
		FandV_response = json.dumps(FandV,indent=4)
		#print FandV_response
		print '---Features and VLAN Configuration: 	' + config_status(FandV,"FandV")

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
		print '---VPC Configuration: 			' + config_status(vpc,"vpc")
		#print vpc_response

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
		print '---Management Information Config: 	' + config_status(mgmt,"mgmt")
		#print mgmt_response

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
		l3pc = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
		l3pc_response = json.dumps(l3pc,indent=4)
		print '---Layer3 Port-Channel Config: 		' + config_status(l3pc,"l3pc")
		#print l3pc_response

		print colors.info('[INFO]') +' END CONFIGURATION PUSH TO ' + switch + "\n\n"