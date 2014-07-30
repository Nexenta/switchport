#!/usr/bin/bash
#
# neetplan module for Inventec-iOS protocol

class inventec_icos:
	#
	#
	def fixed_lines (self,sw_proto,np):
		return []
		
	#
	# return lines for the specified sp_name and profile_name
	#
	def profile_lines (self,np,sp_name,pname):
		lines = []
		profile=np['profiles'].get(pname)
		n_vlans = len(profile)
		
		id = []
		for vlan_name in profile:
			id.append(str(np['vlans'].get(vlan_name)['vlan']))
	
		if n_vlans > 1:
			lines.append('vlan participation include  '+','.join(id))
			lines.append('vlan acceptframe vlanonly')
			lines.append('vlan ingressfilter')
		elif np['single-vlan-mode'] == 'access':
			lines.append('vlan participation include '+id[0])
			lines.append('vlan pvid '+id[0])
			lines.append('vlan acceptframe admituntaggedonly')
			lines.append('vlan ingressfilter')
		else:
			lines.append('vlan participation include  '+id[0])
			lines.append('vlan acceptframe vlanonly')
			lines.append('vlan ingressfilter')
				
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
