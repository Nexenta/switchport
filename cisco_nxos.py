#!/usr/bin/bash
#
# neetplan module for Cisco-NXOS protocol

class cisco_nxos:
	#
	# Cisco NXOS requires queues be created globally
	# MTU is assigned to queues
	#
	# First find the replicast % of the total bandwdith and its cos
	# then it is mostly a static script with only a few variable fill-ins
	#
	def fixed_lines (self,sw_proto,np):
		rep_bw = 0
		total_weight = 0
		for vlan_name in np['vlans'].keys():
			v = np['vlans'].get(vlan_name)			
			if v['no-drop'] == 'true':
				replicast_cos = v['cos']
				rep_w = v['weight']
			total_weight = total_weight + v['weight']
		if rep_w == 0:
			print "Error. Repicast bandwidth not assigned"
			exit(4)
		rep_percent = int(rep_w*100/total_weight)
		def_percent = 100 - rep_percent

		lines = []
		lines.append('class-map type qos class-relicast')
		lines.append('match cos '+str(replicast_cos))
		lines.append('set qos-group 1')
		lines.append('class class-default')
		lines.append('set qos-group 0')
		lines.append('system qos')
		lines.append('service-policy type qos replicast-in-policy')
		lines.append('class-map type queuing class-replicast')
		lines.append('match qos-group 1')
		lines.append('class-map type queing class-default')
		lines.append('match qos-group 0')
		lines.append('policy-map type queuing policy-bw')
		lines.append('class type queuing  class-replicast')
		lines.append('bandwidth percent '+str(rep_percent))
		lines.append('class type queuing class-default')
		lines.append('bandwidth percent '+str(def_percent))
		lines.append('system qos')
		lines.append('service-policy type queuing input policy-bw')
		lines.append('service-policy type queuing output policy-bw')
		lines.append('class-map type network-qos class-replicast')
		lines.append('match qos-group 1')
		lines.append('class-map clas-default')
		lines.append('policy-map type network-qos replicast-default-nq-policy')
		lines.append('class class-replicast')
		lines.append('pause no-drop')
		lines.append('mtu 9000')
		lines.append('class class-default')
		lines.append('mtu 9000') 
		
		return lines
		
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
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+','.join(id))
		elif np['single-vlan-mode'] == 'access':
			lines.append('switchport mode access')
			lines.append('switchport access vlan '+id[0])
		else:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+id[0])
				
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
