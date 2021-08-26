
# Check smb version and server info

## nmap

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ sudo nmap -p445 --script smb-protocols 192.168.200.100 -O -Pn                                                                                   130 ⨯
	Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
	Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-19 15:55 EDT
	Nmap scan report for valhalla.local (192.168.200.100)
	Host is up (0.00040s latency).

	PORT    STATE SERVICE
	445/tcp open  microsoft-ds
	MAC Address: 00:0C:29:7F:AE:D8 (VMware)
	Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
	Device type: general purpose
	Running: Microsoft Windows 2012
	OS CPE: cpe:/o:microsoft:windows_server_2012:r2
	OS details: Microsoft Windows Server 2012 or Windows Server 2012 R2
	Network Distance: 1 hop

	Host script results:
	| smb-protocols: 
	|   dialects: 
	|     NT LM 0.12 (SMBv1) [dangerous, but default]
	|     2.02
	|     2.10
	|     3.00
	|_    3.02

	OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 2.26 seconds



## metasploit

	msf6 auxiliary(scanner/smb/smb_version) > run
	[*] 192.168.200.100:445   - SMB Detected (versions:1, 2, 3) (preferred dialect:SMB 3.0.2) (signatures:required) (uptime:15m 42s) (guid:{0e6e2ca3-2bd4-4307-8e35-70564748263c}) (authentication domain:VALHALLA)
	[+] 192.168.200.100:445   -   Host is running Windows 2012 R2 Standard Evaluation (build:9600) (name:ODIN) (domain:VALHALLA)
	[*] valhalla.local:       - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	msf6 auxiliary(scanner/smb/smb_version) >


## crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
