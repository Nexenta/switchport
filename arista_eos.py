#!/usr/bin/bash
#
# neetplan module for Aristas-EOS protocol


class arista_eos:
	#
	# Arista-EOS requires no configuration lines independent of interface configuration
	#
	def fixed_lines (self,sw_proto,np):
		lines = []
		return lines
		
	#
	# return lines for the specified profile_name
	#
	def profile_lines (self,np,pname):
		lines = []
		profile=np['profiles'].get(pname)
		n_vlans = len(profile)
		
		total_weight = 0
		no_drop_cos = 4
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
			if v['no-drop'] == 'true':
				no_drop_cos = cos[0]

		lines.append('mtu 9000')	
		if n_vlans > 1:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+','.join(id))
		elif np['single-vlan-mode'] == 'access':
			lines.append('switchport mode access')
			lines.append('switchport access vlan '+id[0])
		else:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+id[0])

		remaining_weight = 100
		for i in range(len(cos)):
			lines.append('tx-queue '+cos[i])
			if i==0:
				lines.append('no priority')
			if i < len(cos)-1:
				percent = int(weight[i])*100/total_weight
				remaining_weight = remaining_weight - percent
			else:
				percent = remaining_weight
			
			lines.append('bandwidth percent '+str(percent))
								
		lines.append('priority-flow-control mode on')
		lines.append('priority-flow-control priority '+no_drop_cos+' no-drop')
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

