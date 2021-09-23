Connect to rpc server

	┌──(kali㉿kali)-[~]
	└─$ rpcclient 192.168.200.100 -U valhalla.local/testuser
	Enter VALHALLA.LOCAL\testuser's password: 
	rpcclient $> srvinfo
			192.168.200.100Wk Sv PDC Tim NT     odin
			platform_id     :       500
			os version      :       6.3
			server type     :       0x80102b
	rpcclient $> 

query for domain users
	
	rpcclient $> enumdomusers
	
query domain user details
	
	user:[printerbug] rid:[0x84d]
	rpcclient $> queryuser 0x84d

query for domain groups
	
	rpcclient $> enumdomgroups

query domain group detail

	rpcclient $> querygroup 0x200
			Group Name:     Domain Admins
			Description:    Designated administrators of the domain
			Group Attribute:7
			Num Members:1

