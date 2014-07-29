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
		profile=np['profiles'].get(pname)
		n_vlans = len(profile)
		
		total_weight = 0
		vname = []
		id = []
		cos = []
		weight = []
		for vlan_name in profile:
			vname.append(vlan_name)
			v = np['vlans'].get(vlan_name)
			id.append(str(v['vlan']))
			cos.append(str(v['cos']))
			w = v['weight']
			total_weight = total_weight + w
			weight.append(str(w))
	
		if n_vlans == 1:
			if np['single-vlan-mode'] == 'access':

				lines.append('switchport mode access')
				lines.append('switchport access vlan '+id[0])
			else:
				lines.append('switchport mode trunk')
				lines.append('switchport trunk allowed vlan '+id[0])
			# set up PFC
			# set up spanning tree edge
		else:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+','.join(id))
			# set up queues
			# get bandwidth %
			# set of PFC/no-drop for replicast
			# set up spanning tree edge
			
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

