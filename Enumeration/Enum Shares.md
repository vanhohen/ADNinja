# Enum Shares

## smbclient

Detect

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ smbclient -L 192.168.200.100 -U valhalla.local/testuser                                                                                           1 ⨯
	Enter VALHALLA.LOCAL\testuser's password: 

			Sharename       Type      Comment
			---------       ----      -------
			ADMIN$          Disk      Remote Admin
			C$              Disk      Default share
			IPC$            IPC       Remote IPC
			NETLOGON        Disk      Logon server share 
			share           Disk      
			SYSVOL          Disk      Logon server share 
	SMB1 disabled -- no workgroup available


Connect

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ smbclient \\\\192.168.200.100\\share -U valhalla.local/testuser
	Enter VALHALLA.LOCAL\testuser's password: 
	Try "help" to get a list of possible commands.
	smb: \> ls
	  .                                   D        0  Sat Aug 14 19:43:34 2021
	  ..                                  D        0  Sat Aug 14 19:43:34 2021
	  projectx.txt                        A       24  Sat Aug 14 20:07:25 2021

					15638527 blocks of size 4096. 13126313 blocks available
	smb: \> get projectx.txt 
	getting file \projectx.txt of size 24 as projectx.txt (11.7 KiloBytes/sec) (average 11.7 KiloBytes/sec)
	smb: \> 


## smbmap

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ smbmap -H 192.168.200.100 -d valhalla.local -u testuser -p Pass123!
	[+] IP: 192.168.200.100:445     Name: valhalla.local                                    
			Disk                                                    Permissions     Comment
			----                                                    -----------     -------
			ADMIN$                                                  NO ACCESS       Remote Admin
			C$                                                      NO ACCESS       Default share
			IPC$                                                    READ ONLY       Remote IPC
			NETLOGON                                                READ ONLY       Logon server share 
			share                                                   READ ONLY
			SYSVOL                                                  READ ONLY       Logon server share 


## smb_enumshares

	msf6 auxiliary(scanner/smb/smb_enumshares) > set smbuser thor
	smbuser => thor
	msf6 auxiliary(scanner/smb/smb_enumshares) > set smbpass Pass123!
	smbpass => Pass123!
	msf6 auxiliary(scanner/smb/smb_enumshares) > set smbdomain valhalla.local
	smbdomain => valhalla.local
	msf6 auxiliary(scanner/smb/smb_enumshares) > set rhosts 192.168.200.100
	rhosts => 192.168.200.100
	msf6 auxiliary(scanner/smb/smb_enumshares) > run

	[-] 192.168.200.100:139   - Login Failed: Unable to negotiate SMB1 with the remote host: Not a valid SMB packet
	[!] 192.168.200.100:445   - peer_native_os is only available with SMB1 (current version: SMB3)
	[!] 192.168.200.100:445   - peer_native_lm is only available with SMB1 (current version: SMB3)
	[+] 192.168.200.100:445   - ADMIN$ - (DISK) Remote Admin
	[+] 192.168.200.100:445   - C$ - (DISK) Default share
	[+] 192.168.200.100:445   - IPC$ - (IPC) Remote IPC
	[+] 192.168.200.100:445   - NETLOGON - (DISK) Logon server share 
	[+] 192.168.200.100:445   - SYSVOL - (DISK) Logon server share 
	[*] 192.168.200.100:      - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed


## crackmaexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 -u thor -p Pass123! -d valhalla.local --shares
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\thor:Pass123! 
	SMB         192.168.200.100 445    ODIN             [+] Enumerated shares
	SMB         192.168.200.100 445    ODIN             Share           Permissions     Remark
	SMB         192.168.200.100 445    ODIN             -----           -----------     ------
	SMB         192.168.200.100 445    ODIN             ADMIN$                          Remote Admin
	SMB         192.168.200.100 445    ODIN             C$                              Default share
	SMB         192.168.200.100 445    ODIN             IPC$                            Remote IPC
	SMB         192.168.200.100 445    ODIN             NETLOGON        READ            Logon server share 
	SMB         192.168.200.100 445    ODIN             SYSVOL          READ            Logon server share 
