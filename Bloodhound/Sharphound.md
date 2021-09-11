# Sharphound

If you want to run Sharphound from a PC that is not joined to the target domain, open a command prompt and run:

	runas /netonly /user:DOMAIN\USER powershell.exe
	Enter the password for DOMAIN\USER:
	Attempting to start powershell.exe as user "DOMAIN\USER" ...
	
Then import Sharpound and run it as normal.

	import-module sharphound.ps1
	invoke-bloodhound -collectionmethod all -domain TARGETDOMAIN
	.\SharpHound.exe --CollectionMethod all -d valhalla.local
	