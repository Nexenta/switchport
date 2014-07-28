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

from arista_eos import arista_eos
from cisco_nxos import cisco_nxos
from inventec_dcos import inventec_dcos
from unknown_switch import unknown_switch

def sw_protocol (p):
	if p == "Arista-EOS":
		return arista_eos()
	if p == "Ciscso-NXOS":
		return cisco_nxos()
	if p == 'Inventec-DCOS':
		return inventec_dcos()
	return unknown_switch()
	
	
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
	print "process_switch",switch_name,"fixed",fixed_lines,"profile",profile_lines
	cmd_file = open (switch_name+".cmd",'w')
	s = np['switches'].get(switch_name)
	switchports_file = open (switch_name+".lldp",'w')
	err = switchports_file.write(s['macaddr'])
	if err != 0:
		print "switchports file write err",err
		exit(2)
	p = s['protocol']
	print "protocol",p
	spc = switch_protocol(s['protocol'])
	for line in fixed_lines:
		cmd_file.write(line)
	profiles = np_profile(switch_name)
	for pname in profiles.keys():
		lines = spc.apply_to_interface_list(profiles[pname],profile_lines[pname])
		for line in lines:
			cmd_file.write(line)
#			write to switchport_file

	switchports_file.close()
	cmd_file.close()
	return 0

		
if len(sys.argv) != 2:
	print "usage:",sys.argv[0],"network-plan-json-file"
	exit(1)
	
	
netplan_js = open(sys.argv[1],'r').read()
np = json.loads(netplan_js)
switches = np_switches()

fixed_lines=dict()
profile_lines=dict()

for sp_name in np['protocols'].keys():
	profile_lines[sp_name] = dict()
	spc = sw_protocol(sp_name)
	fixed_lines[sp_name] = spc.fixed_lines(spc,np)
	for pname in np['profiles'].keys():
		lines = spc.profile_lines(np,sp_name,pname)
		profile_lines.get(sp_name)[pname] = lines
		f = open (sp_name+"."+pname+".cmd","w")
		for line in profile_lines.get(sp_name)[pname]:
			f.write(line)
		f.close()		


for s in switches:
	sp_name = np_protocol(s)
	f = fixed_lines.get(sp_name)
	p = profile_lines.get(sp_name)
	process_switch(np,s,f,p)
	
exit(0)





	

	




	




	
		

