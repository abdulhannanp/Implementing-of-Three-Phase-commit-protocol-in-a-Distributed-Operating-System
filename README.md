
  



Tools Used:
Pycharm 2017 3.3
Python 3.4




How to run the program?
1.Download the Pycharm 2017 3.3 version and following the installer wizard and finish the installation.
2.Download and unzip the folder into your Pycharm Projects folder following the path used for installation.
3.Just click on one of the python files and the entire project should open up in the Pycharm application.
4.Now, right click on the Server_Chat.py file and click Run.
5.The console window below should display the message “…Listening…”
6.Once done, right click on the Client_Chat.py file and click Run.
7.Now, the console window will ask u for a hostname and port number.
8.Specify the hostname as localhost (ideally your desired host) and the port number as 25000.
9.You are now connected to the server and the confirmation can be found on the server console window along with the thread assigned for the client.
10.The chat room window would open in the taskbar. Click on it to bring it to the front if it does not pop up.
11.In the window, provide one of the following usernames to go through:
{"Jo","System","Professor",
"TA","Johnsy","Pooja","God"}
12.The server should have sent a welcome message now and now you are ready to chat with the other clients (if any).
13.Similarly, run 3 other clients and type in the messages.

14.You will see that all the messages get broadcasted to all the other clients and shows the message when one of the clients get disconnected.

15.All the information is also printed in the server console in the HTTP format  

16.If you the client is ready to quit, the {exit} message can be typed in or the window can be closed directly.
17.The server will show that the client has disconnected.



18. Run the Server_Chat.py, Coordinator.py and Participant.py (3 of its instances) programs and provide the valid username.
19. Click Request in Coordinator and provide user inputs from all the participant windows using COMMIT or ABORT buttons
20. If Global-Commit, the string will be written to the files created.
21. If Global-Abort, an empty line gets inserted into the file indicating that the string did not get committed.
22. If the participants have voted to commit the transaction, the coordinator sends a request to acknowledge the same.
23. The participant waits for this acknowledgement from the coordinator for 30 seconds and if no response is received, it assumes that the coordinator has crashed.
24. The participants are now in pre-commit state and will be prompted to click the ACK button.
25. The coordinator then waits for 30 seconds to send the global state message to all the participants.
26. If the ack timer times out, then the coordinator considers that the participant has crashed and sends the commit message. 

SCREENSHOTS

GLOBAL COMMIT SCENARIO










GLOBAL ABORT SCENARIO:





TIMEOUT SCENARIOS

INIT STATE AT PARTICIPANT







PARTICIPANTS CRASHED ASSUMPTION – ACK



COORDINATOR CRASH ASSUMPTION



(i)IF NO RESPONSE FROM PARTICIPANTS - ABORT



(ii)IF OTHER PARTICIPANTS IN COMMIT STATE – COMMIT:




STRING WRITTEN TO FILE:



IF CLIENT WITH THAT NAME ALREADY EXISITS:







COORDINATOR ASSUMES PARTICIPANTS CRASHED:






