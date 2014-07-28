#!/usr/bin/bash
#
# neetplan module for Cisco-NXOS protocol

class cisco_nxos:
	#
	# Cisco NXOS requires queues be created globally
	# MTU is assigned to queues
	#
	def fixed_lines (self,sw_proto,np):
		return []
		
	#
	# return lines for the specified sp_name and profile_name
	#
	def profile_lines (self,np,sp_name,pname):
		lines = []
		lines.append("need to do something with "+pname+" for "+sp_name)
		#
		# for each vlan
		#		...
		#
		return lines
		
	#
	# apply interface list to lines[]
	#
	def apply_to_interface_list (self,interface_list,lines):
		applied_lines = "interface ethernet "+str(interface_list)
		applied_lines.append(lines)
		
		return applied_lines