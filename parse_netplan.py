#!/usr/bin/python

#!/usr/bin/python
#
# netplan_test_parse.py <network-plan-json-filename>
#
# Parses a network plan and prints the info back out
# this prototypes usage of python json support and the specific schema
# forthe network plan. See netplan-example.json for syntax.
#


import sys,json
from array import *

np = dict()


def np_switches ():
	return np['switches'].keys()
	
def np_profiles (switch):
	return np['switches'].get(switch)['profiles']
	
def np_macaddr (switch):
	return np['switches'].get(switch)['macaddr']
	
def np_protocol (switch):
	return np['switches'].get(switch)['protocol']
	
def np_profile (switch):
	return np['switches'].get(switch)['profiles']
	
def np_switchports (switch,profile):
	return np['switches'].get(switch)['profiles'].get(profile)
	
def np_profile_vlans (profile):
	return np['profiles'].get(profile)
	
def np_vlans ():
	return np['vlans'].keys()
	
def np_vlan_id (vlan):
	return np['vlans'].get(vlan)['vlan']
	
def np_vlan_cos (vlan):
	return np['vlans'].get(vlan)['cos']	
	
def np_vlan_weight (vlan):
	return np['vlans'].get(vlan)['weight']		

import arista_eos
import cisco_nxos
import inventec_dcos
import unknown_switch

def switch_protocol (p):
	print "switch_protocol",p
	if p == "Arista-EOS":
		return arista_eos()
	if p == "Ciscso-NXOS":
		return cisco_nxos()
	if p == 'Inventec-DCOS':
		return inventec_dcos()
	return unknown_switch()


#
# process a single switch in the network plan
# The following files are created
#		<switch-name>.cmd			Command file for this switch to configure replicast
#									This file contains the fixed lines, and interface
#									configurations for all pre-configured switchports
#		<switch-name>.lldp			LLDP identification info:
#									1st line: macaddr that identifies the switch
#									remaining lines:
#										interface name and identifying lldp attribute
# 
def process_switch (np,switch_name,fixed_lines,profile_lines):
	cmd_file = open (switch_name+".cmd",'w')
	s = np['switches'].get(switch)
	print "s",s
	switchports_file = open (switch_name,".lldp")
	switchports_file.write(s['macaddr']
	p = s['protocol']
	print "protocol",p
	spc = switch_protocol(s['protocol'])
	for line in fixed_lines:
		cmd_file.write(line)
	profiles = np_profiles(switch_name)
	for profile-name in profiles.keys():
		lines = spc.apply_to_interface_list(profiles[profile_name],profile_lines[profile-name])
		for line in lines:
			cmd_file.write(line)
#			write to switchport_file

	switchport_file.close()
	cmd_file.close()
	return 0

		
if len(sys.argv) != 2:
	print "usage:",sys.argv[0],"network-plan-json-file"
	exit(1)
	
	
netplan_js = open(sys.argv[1],'r').read()
np = json.loads(netplan_js)
switches = np_switches()


for sp_name in np['protocols'].keys():
	spc = swith_protocol()
	fixed_lines[sp-name] = spc.fixed_lines(spc,np)
	for profile-name in np['profiles'].keys():
		profile_lines[sp_name][profile_name] = spc.profile_lines(np,sp_name,profile-name)
		f = open (sp_name+"."+profile_name+".cmd","w")
		for line in profile_lines[sp_name][profile_name]:
			f.write(line)
		f.close()		


for s in switches:
	sp_name = s['protocol']
	process_switch(np,s,fixed_lines[sp_name],profile_lines[sp_name])
	
exit(0)





	

	




	




	
		

