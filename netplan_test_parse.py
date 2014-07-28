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

class netplan_vlan:
	id = 0; # 0..4094
	cos = 0; # 0..7
	weight = 100; # share is weight/total(weight)
	
	
class netplan_switch:
	name = None;
	macaddr = None;
	protocol = None;
	profiles = []; # array of profile names switchport list lists
	

def print_switch (sw):
	print sw.name,sw.macaddr,sw.protocol,sw.profiles
	

def sub_dict (subd):
	print subd.__class__
		
if len(sys.argv) != 2:
	print "usage:",sys.argv[0],"network-plan-json-file"
	exit(1)
	
	
netplan_js = open(sys.argv[1],'r').read()
np = json.loads(netplan_js)
switches = np_switches()

for s in switches:
	sw = netplan_switch()
	sw.name = s;
	sw.macaddr = np_macaddr(s);
	sw.protcol = np_protocol(s);
	sw.profiles = np_profiles(s);
	print_switch (sw);
	
	for p in sw.profiles:
		vlans = np_profile_vlans(p)
		for v in vlans:
			print s,".",p,"-->",np_switchports(s,p),"vlan",v
			
			
for v in np_vlans():
	print "vlan",np_vlan_id(v),"cos",np_vlan_cos(v),"weight",np_vlan_weight(v)
	
sub_dict(np['switches'])


	

	




	




	
		

