# WinRS

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