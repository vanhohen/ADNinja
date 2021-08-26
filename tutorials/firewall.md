# Firewall

check firewall status

```text
PS C:\Users\testuser\Desktop> netsh advfirewall show allprofiles state

Domain Profile Settings:
----------------------------------------------------------------------
State                                 ON

Private Profile Settings:
----------------------------------------------------------------------
State                                 ON

Public Profile Settings:
----------------------------------------------------------------------
State                                 ON
Ok.
```

Disable firewall

```text
PS C:\Users\testuser\Desktop> netsh advfirewall set allprofiles state off
Ok.

PS C:\Users\testuser\Desktop> netsh advfirewall show allprofiles state
Domain Profile Settings:
----------------------------------------------------------------------
State                                 OFF

Private Profile Settings:
----------------------------------------------------------------------
State                                 OFF

Public Profile Settings:
----------------------------------------------------------------------
State                                 OFF
Ok.
```

