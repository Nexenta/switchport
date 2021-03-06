#!/usr/bin/bash
#
# neetplan module for Inventec-iOS protocol

class inventec_icos:
	#
	#
	def fixed_lines (self,switch_name,sw_proto,np):
		return []
		
	#
	# return lines for the specified sp_name and profile_name
	#
	def profile_lines (self,switch_name,np,pname):
		lines = []
		profile=np['profiles'].get(pname)
		n_vlans = len(profile)
		
		id = []
		weight = []
		total_weight = 0
		no_drop_cos = 9
		for vlan_name in profile:
			id.append(str(np['vlans'].get(vlan_name)['vlan']))
			v = np['vlans'].get(vlan_name)
			weight.append(v['weight'])
			total_weight = total_weight + v['weight']
			if v.get('no-drop','false') == 'true':
				no_drop_cos=v['cos']
			
		if no_drop_cos == 9:
			lines.append("Error: no-drop must be set for exactly one vlan")
		
		if n_vlans > 1:
			lines.append('vlan participation include  '+','.join(id))
			lines.append('vlan acceptframe vlanonly')
			pc = []
			pc_left = 100
			len_w = len(weight)
			for i in range(len_w-1):
				pc_i = int(weight[i]*100/total_weight)
				pc_left = pc_left - pc_i
				pc.append(str(pc_i))
			pc.append(pc_left)
			#
			#set bandwidth percents (pc[] is percent per traffic-class
			#which is close, but not exactly whatis needed. Research still in progress
			#
		elif np['single-vlan-mode'] == 'access':
			lines.append('vlan participation include '+id[0])
			lines.append('vlan pvid '+id[0])
			lines.append('vlan priority '+str(no_drop_cos))
			lines.append('vlan acceptframe admituntaggedonly')
		else:
			lines.append('vlan participation include  '+id[0])
			lines.append('vlan acceptframe vlanonly')

		lines.append('vlan ingressfilter')	
		#spanning tree	
		lines.append('datacenter-bridging')
		lines.append('priority-flow-control mode on')
		lines.append('priority-flow-control priority '+str(no_drop_cos)+' no-drop')	
		lines.append('exit')
		lines.append('exit')	
		return lines
		
	#
	# apply interface list to lines[]
	#
	def apply_to_interface_list (self,interface_list,lines):
		applied_lines = []
		for interface in interface_list:
			applied_lines.append("interface "+interface)
			for line in lines:			
				applied_lines.append(line)
		
		return applied_lines
