# Enum Local users

## rpcclient

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ rpcclient -U testuser%Pass123! 192.168.200.100                                                                                                    1 ⨯
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[danj] rid:[0x451]
user:[adamb] rid:[0x452]
user:[alans] rid:[0x453]
.
.
.
.
user:[davidb1] rid:[0x547]
user:[roastme] rid:[0x836]
user:[kerberoastme] rid:[0x844]
user:[testuser] rid:[0x845]
user:[dontmindme] rid:[0x847]
user:[iwouldmind] rid:[0x848]
user:[mrblack] rid:[0x849]
```

## impacket-lookupsid

```text
┌──(kali㉿kali)-[~/Desktop/ADAbuse]
└─$ /usr/bin/impacket-lookupsid valhalla/thor:Pass123\!@192.168.200.110
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Brute forcing SIDs at 192.168.200.110
[*] StringBinding ncacn_np:192.168.200.110[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-3401829504-2746700306-4210517594
500: THOR\Administrator (SidTypeUser)
501: THOR\Guest (SidTypeUser)
513: THOR\None (SidTypeGroup)
1000: THOR\win7 (SidTypeUser)
```

