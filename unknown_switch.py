#!/usr/bin/bash
#
# Dummy netplan module that is catchall for unknown switches
#
# If implementing your own switch module, none of your methods should produce any
# effects other than returning a list of lines.
#


class unknown_switch:
	#
	# This method must generate all commands which are interface independent
	# (which would be the first commands executed) for this switch protocol
	#
	def fixed_lines (self,switch_name,sw_proto,np):
		lines = []
		lines.append('Switch protocol not supported')
		return lines
		
	#
	# return lines for the specified profile_name, identifying the interfaces
	# is handled outside of this routine.
	#
	# A checklist of issues to be addressed:
	#	Set up PFC/no-drop for replicast (if not handled by fixed_lines)
	#	Set up MTU 9000 (if not handled by fixed_lines)
	#	Enable the set of vlans for the port
	#	set up weighted round-robin over those vlans
	#	enable lldp (if not handled by fixed_lines)
	#	optionally supporess spanning tree for this port (its an edge port)
	#
	def profile_lines (self,switch_name,np,pname):
		lines = []
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
