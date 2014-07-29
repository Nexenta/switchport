#!/usr/bin/bash
#
# neetplan module for Aristas-EOS protocol

class arista_eos:
	#
	# Arista-EOS requires no configuration lines independent of interface configuration
	#
	def fixed_lines (self,sw_proto,np):
		lines = []
		lines.append("sw_proto "+str(sw_proto))
		return lines
		
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
		applied_lines = []
		for interface in interface_list:
			applied_lines.append("interface ethernet "+interface)
			for line in lines:			
				applied_lines.append(line)
		
		return applied_lines

