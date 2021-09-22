RDP to machines. To enable NLA use:

https://www.virtuesecurity.com/enable-network-level-access-windows-rdp/


User need to have RDP permission. To enable it you can add user to "Remote Desktop Users" group. You can give it with AD also

	>net localgroup "Remote Desktop Users" testuser /add


RDP with user-pass

	┌──(kali㉿kali)-[/usr/share/set/src/powershell]
	└─$ xfreerdp /v:192.168.200.112 /u:testuser /p:'Pass123!' /d:valhalla.local  
	