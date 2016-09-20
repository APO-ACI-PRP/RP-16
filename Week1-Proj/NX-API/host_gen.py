#!/usr/bin/env python

import csv
import sys
import json
import requests
from collections import defaultdict

def hostfile(hostdict):
	host_dict = hostdict

	file_name = "/etc/ansible/hosts"

	with open(file_name, 'w') as hostfile:
		hostfile.write("[all:vars] \n")
		hostfile.write("configdir=/home/cisco/Project/configs \n")
		hostfile.write("[switches]\n")
		for switches in host_dict:
			hostfile.write(switches+"\n")