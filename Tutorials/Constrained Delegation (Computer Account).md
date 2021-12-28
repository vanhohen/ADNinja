Lets say during our enumeration we found computer object given rights to constrained delegation. 

	PS C:\Users\testuser\Desktop> Get-DomainComputer -Identity loki
	
	logoncount                    : 80
	badpasswordtime               : 1/1/1601 2:00:00 AM
	distinguishedname             : CN=LOKI,CN=Computers,DC=child,DC=valhalla,DC=local
	objectclass                   : {top, person, organizationalPerson, user...}
	badpwdcount                   : 0
	lastlogontimestamp            : 12/26/2021 6:11:53 PM
	objectsid                     : S-1-5-21-988250465-358338136-668553488-1105
	samaccountname                : LOKI$
	localpolicyflags              : 0
	codepage                      : 0
	samaccounttype                : MACHINE_ACCOUNT
	countrycode                   : 0
	cn                            : LOKI
	accountexpires                : NEVER
	whenchanged                   : 12/28/2021 5:22:22 PM
	instancetype                  : 4
	usncreated                    : 13030
	objectguid                    : 9c39686b-dc6a-4752-bafd-2ae63f50facc
	operatingsystem               : Windows 10 Pro
	operatingsystemversion        : 10.0 (10586)
	lastlogoff                    : 1/1/1601 2:00:00 AM
	msds-allowedtodelegateto      : {cifs/kabil.child.valhalla.local/child.valhalla.local, cifs/kabil.child.valhalla.local, cifs/KABIL,
									cifs/kabil.child.valhalla.local/CHILD...}
	objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=valhalla,DC=local
	dscorepropagationdata         : 1/1/1601 12:00:00 AM
	serviceprincipalname          : {TERMSRV/LOKI, TERMSRV/loki.child.valhalla.local, RestrictedKrbHost/LOKI, HOST/LOKI...}
	lastlogon                     : 12/28/2021 7:23:32 PM
	iscriticalsystemobject        : False
	usnchanged                    : 24608
	useraccountcontrol            : WORKSTATION_TRUST_ACCOUNT, TRUSTED_TO_AUTH_FOR_DELEGATION
	whencreated                   : 11/26/2021 7:15:43 AM
	primarygroupid                : 515
	pwdlastset                    : 12/27/2021 10:12:03 PM
	msds-supportedencryptiontypes : 28
	name                          : LOKI
	dnshostname                   : loki.child.valhalla.local