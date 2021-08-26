# Checking your rights for remote device

## SMB\_Login

```text
msf6 auxiliary(scanner/smb/smb_login) > set smbuser administrator
smbuser => administrator
msf6 auxiliary(scanner/smb/smb_login) > set smbpass Pass123!
smbpass => Pass123!
msf6 auxiliary(scanner/smb/smb_login) > set smbdomain valhalla.local
smbdomain => valhalla.local
msf6 auxiliary(scanner/smb/smb_login) > run
[*] 192.168.200.100:445   - 192.168.200.100:445 - Starting SMB login bruteforce
[+] 192.168.200.100:445   - 192.168.200.100:445 - Success: 'valhalla.local\administrator:Pass123!' Administrator
[*] valhalla.local:445    - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/smb/smb_login) > 
```

## Crackmapexec

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ crackmapexec smb valhalla.local -u administrator -p Pass123!                                                                                   1 ⚙
SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
SMB         192.168.200.100 445    ODIN             [+] valhalla.local\administrator:Pass123! (Pwn3d!)
```

