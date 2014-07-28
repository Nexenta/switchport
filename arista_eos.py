#!/usr/bin/bash
#
# neetplan module for Aristas-EOS protocol

class arista_eos:
	#
	# Arista-EOS requires no configuration lines independent of interface configuration
	#
	def fixed_lines ()
		return []
		
	#
	# return lines for the specified sp_name and profile_name
	#
	def profile_lines (np,sp_name,profile-name)
		lines = []
		#
		# for each vlan
		#		...
		#
		return lines
		
	#
	# apply interface list to lines[]
	#
	def apply_to_interface_list (interface_list,lines):
		applied_lines = "interface ethernet "+str(interface_list)
		applied_lines.append(lines)
		
		return applied_lines

