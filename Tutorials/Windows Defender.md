
# Windows Defender

Check stat

	F:\test>sc query WinDefend

	SERVICE_NAME: WinDefend
			TYPE               : 20  WIN32_SHARE_PROCESS
			STATE              : 4  RUNNING
									(STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
			WIN32_EXIT_CODE    : 0  (0x0)
			SERVICE_EXIT_CODE  : 0  (0x0)
			CHECKPOINT         : 0x0
			WAIT_HINT          : 0x0

Stop 

	F:\test>sc stop WinDefend

	SERVICE_NAME: WinDefend
			TYPE               : 20  WIN32_SHARE_PROCESS
			STATE              : 4  RUNNING
									(STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
			WIN32_EXIT_CODE    : 0  (0x0)
			SERVICE_EXIT_CODE  : 0  (0x0)
			CHECKPOINT         : 0x0
			WAIT_HINT          : 0x0

Check 

	F:\test>sc query WinDefend

	SERVICE_NAME: WinDefend
			TYPE               : 20  WIN32_SHARE_PROCESS
			STATE              : 1  STOPPED
			WIN32_EXIT_CODE    : 0  (0x0)
			SERVICE_EXIT_CODE  : 0  (0x0)
			CHECKPOINT         : 0x0
			WAIT_HINT          : 0x0



[Credit](https://superuser.com/a/1046300)