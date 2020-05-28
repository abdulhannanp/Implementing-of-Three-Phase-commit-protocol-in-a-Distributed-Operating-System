
  



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






CITATIONS:
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
https://www.youtube.com/watch?v=Iq1dM4-jEX8
https://stackoverflow.com/questions/26275994/write-line-with-timestampmessage-to-file
http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
https://stackoverflow.com/questions/919897/how-to-find-a-thread-id-in-python
https://www.binarytides.com/code-chat-application-server-client-sockets-python/ http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
https://www.youtube.com/watch?v=GZyQmkxH8as
https://www.youtube.com/watch?v=ZwxTGGEx-1w
https://github.com/JackZProduction/python_chat
https://wiki.python.org/moin/TkInter
https://www.tutorialspoint.com/python/python_gui_programming.htm
http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
https://stackoverflow.com/questions/10556479/running-a-tkinter-form-in-a-separate-thread/10556698#10556698
https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop
https://stackoverflow.com/questions/26275994/write-line-with-timestampmessage-to-file
https://stackoverflow.com/questions/33235626/saving-to-msg-file-in-python-or-alternatively-sending-mail-to-the-file-system
https://pythonspot.com/tk-message-box/
hhttps://stackoverflow.com/questions/30396709/python-3-encoding-or-errors-without-a-string-argument/30396845#30396845
https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
https://github.com/cloudera/impyla/issues/238
https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
https://stackoverflow.com/questions/4005796/attributeerror-str-object-has-no-attribute-append
https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
https://stackoverflow.com/questions/3752618/python-adding-element-to-list-while-iterating
https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list
https://stackoverflow.com/questions/44901806/python-error-message-io-unsupportedoperation-not-readable
https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist
https://stackoverflow.com/questions/18406165/creating-a-timer-in-python
https://stackoverflow.com/questions/21242848/how-to-add-timer-with-start-stop-gui-in-python
https://stackoverflow.com/questions/41452819/python-list-append-in-for-loop/41452829
https://swcarpentry.github.io/python-novice-inflammation/03-lists/
https://www.python-course.eu/python3_list_manipulation.php
https://stackoverflow.com/questions/13685201/how-to-add-hours-to-current-time-in-python
https://stackoverflow.com/questions/3787908/python-determine-if-all-items-of-a-list-are-the-same-item
https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
