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

		
if len(sys.argv) != 2:
	print "usage:",sys.argv[0],"network-plan-json-file"
	exit(1)
	
	
netplan_js = open(sys.argv[1],'r').read()
np = json.loads(netplan_js)
switches = np_switches()

for s in switches:
	print s,np_macaddr(s),np_protocol(s),np_profiles(s)	
	for p in  np_protocol(s):
		print "s",s,"p",p
		vlans = np_profile_vlans(p)
		for v in vlans:
			print s,".",p,"-->",np_switchports(s,p),"vlan",v
						
for v in np_vlans():
	print "vlan",np_vlan_id(v),"cos",np_vlan_cos(v),"weight",np_vlan_weight(v)
	
sub_dict(np['switches'])


	

	




	




	
		

