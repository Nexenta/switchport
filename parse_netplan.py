#!/usr/bin/python

#!/usr/bin/python
#
# netplan_test_parse.py <network-plan-json-filename>
#
# Parses a network plan and prints the info back out
# this prototypes usage of python json support and the specific schema
# forthe network plan. See netplan-example.json for syntax.
#


import os,sys,json,re
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
#		out/<switch-name>.cmd		Command file for this switch to configure replicast
#									This file contains the fixed lines, and interface
#									configurations for all pre-configured switchports
#		out/<switch-name>.lldp		LLDP identification info:
#									1st line: macaddr that identifies the switch
#									remaining lines:
#										interface name and identifying lldp attribute
# 


		
if len(sys.argv) != 2:
	print "usage:",sys.argv[0],"network-plan-json-file"
	exit(1)
	
	
netplan_js = open(sys.argv[1],'r').read()
np = json.loads(netplan_js)

try:
	os.mkdir("out")
except:
	pass


for sp_name in np['protocols'].keys():
	spc = sw_protocol(sp_name)
	for pname in np['profiles'].keys():
		f = open ("out/"+sp_name+"."+pname+".cmd","w")
		lines = spc.profile_lines(np,sp_name,pname)
		for line in lines:
			f.write(line+"\n")
		f.close()		



switchports_file = open ("out/lldp",'w')
for switch_name in np['switches'].keys():
	sp_name = np_protocol(switch_name)
	spc = sw_protocol(sp_name)
	fixed_lines = spc.fixed_lines(spc,np)
	
	cmd_file = open ("out/"+switch_name+".cmd",'w')
		
	for line in fixed_lines:
		err = cmd_file.write(line+"\n")
		if err:
			print "cmdfile write error",err
			exit(2)
		
	spc = sw_protocol(sp_name)
	profiles = np_profile(switch_name)
	protocol_name = np_protocol(switch_name)
	for pname in profiles.keys():
		plines = spc.profile_lines(np,sp_name,pname)
		interfaces = np_switchports(switch_name,pname).split(',')
		for interface in interfaces:
			prs = np['protocols']
			protocol = prs.get(protocol_name)
			lldp_maps = protocol['lldp-map']
			for map in lldp_maps:
				m=re.match(map[0],interface)
				if m:
					subbed = "'" + map[1].replace('*',interface)+"'"
					line = np_macaddr(switch_name)+" "+subbed+" --> "+interface+"\n"
					switchports_file.write(line)
					break
		lines = spc.apply_to_interface_list(interfaces,plines)
		for line in lines:
			cmd_file.write(line+"\n")


	cmd_file.close()

switchports_file.close()	
exit(0)





	

	




	




	
		

