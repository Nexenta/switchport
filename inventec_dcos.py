#!/usr/bin/bash
#
# neetplan module for Inventec-DCOS protocol

class inventec_dcos:
	#
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