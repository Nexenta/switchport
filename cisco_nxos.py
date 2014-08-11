#!/usr/bin/bash
#
# neetplan module for Cisco-NXOS protocol
#
# TODO: we need to create service-policies for each possible switchport type
# and then apply that policy to that switchport during profile_lines()
# 
# Current code just sets up a single policy and applies it to all replicast
# enabled switchports
#

class cisco_nxos:
	#
	# Cisco NXOS requires queues be created globally
	# MTU is assigned to queues
	#
	# First find the replicast % of the total bandwdith and its cos
	# then it is mostly a static script with only a few variable fill-ins
	#
	def fixed_lines (self,sw_proto,np):
		lines = []
		replicast_cos = 1000
		for vlan_name in np['vlans'].keys():
			v = np['vlans'].get(vlan_name)
			if v['no-drop'] == 'true':
				replicast_cos = v['cos']
				break
		if replicast_cos == 1000:
			print "Error: A no-drop vlan must be defined"
			exit(4)
		lines.append('configure')
		lines.append('write erase')
		lines.append('class-map type qos class-replicast')
		lines.append('match cos '+str(replicast_cos))
		lines.append('exit')
		lines.append('policy-map type qos replicast-in-policy')
		lines.append('class class-replicast')
		lines.append('set qos-group 1')
		lines.append('exit')
		lines.append('exit')
		lines.append('class-map type queuing class-replicast')
		lines.append('match qos-group 1')
		lines.append('exit')
		lines.append('class-map type network-qos class-replicast')
		lines.append('match qos-group 1')
		lines.append('exit')
		lines.append('policy-map type network-qos replicast-netpolicy')
		lines.append('class type network-qos class-replicast')
		lines.append('pause no-drop')
		lines.append('mtu 9000')
		lines.append('class type network-qos class-default')
		lines.append('mtu 9000') 
		lines.append('exit')
		lines.append('exit')
		for profile_name in np['profiles'].keys():
			total_weight = 0
			rep_weight = 0
			replicast_cos
			for vlan_name in np['profiles'].get(profile_name):
				v = np['vlans'].get(vlan_name)
				total_weight = total_weight + v['weight']
				if v['no-drop'] == 'true':
					rep_weight = v['weight']
			rep_percent = int(rep_weight*100/total_weight)
			def_percent = 100 - rep_percent
			lines.append('policy-map type queuing replicast-policy-'+profile_name)
			lines.append('class type queuing  class-replicast')
			lines.append('bandwidth percent '+str(rep_percent))
			lines.append('class type queuing class-default')
			lines.append('bandwidth percent '+str(def_percent))
			lines.append('exit')
			lines.append('exit')


		lines.append('system qos')
		lines.append('service-policy type network-qos replicast-netpolicy')
		lines.append('exit')		
		return lines
		
	#
	# return lines for the specified sp_name and profile_name
	#
	def profile_lines (self,np,pname):
		lines = []
		profile=np['profiles'].get(pname)
		n_vlans = len(profile)
		
		id = []
		for vlan_name in profile:
			id.append(str(np['vlans'].get(vlan_name)['vlan']))
	
		if n_vlans > 1:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+','.join(id))
			#lines.append('spanning-tree port-type edge trunk')
		elif np['single-vlan-mode'] == 'access':
			lines.append('switchport mode access')
			lines.append('switchport access vlan '+id[0])
			#lines.append('spanning-tree port-type edge')
		else:
			lines.append('switchport mode trunk')
			lines.append('switchport trunk allowed vlan '+id[0])
			#lines.append('spanning-tree port-type edge trunk')
				

		lines.append('priority-flow-control mode on')
		lines.append('service-policy input replicast-in-policy')
		lines.append('service-policy type queuing input replicast-policy-'+pname)
		lines.append('service-policy type queuing output replicast-policy-'+pname)
		lines.append('exit')

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
