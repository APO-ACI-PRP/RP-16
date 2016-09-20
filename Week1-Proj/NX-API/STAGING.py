#!/usr/bin/python 

import json
import sys
import os
import VPC_CONFIG_PUSH

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Host, Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

import file_builder

csv_input = sys.argv

try:
	vpc_info = open(csv_input[1])
except IOError:
	print "ERROR UPLOADING VPC FILE"
	#raise
	sys.exit(1)
except IndexError:
	print "[ERROR] INCORRECT USAGE \n\n Usage: " + csv_input[0] + " <vpc config file>.csv <vlan config file>.csv \n"
	#raise
	sys.exit(1)

try:
	vlan_info = open(csv_input[2])
except IOError:
	print "ERROR UPLOADING VLAN FILE"
	#raise
	sys.exit(1)
except IndexError:
	print "[ERROR] INCORRECT USAGE \n\n Usage: " + csv_input[0] + " <vpc config file>.csv <vlan config file>.csv \n"
	#raise
	sys.exit(1)



file_builder.build(csv_input[1],csv_input[2])

variable_manager = VariableManager()
loader = DataLoader()

inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')
playbook_path = '/etc/ansible/config-builder.yml'

if not os.path.exists(playbook_path):
	print '[INFO] The playbook does not exist'
	sys.exit()

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='local', module_path=None, forks=100, remote_user='stephen', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None, become_user='root', verbosity=None, check=False)


passwords = {}

pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

results = pbex.run()

VPC_CONFIG_PUSH.nx_staging()