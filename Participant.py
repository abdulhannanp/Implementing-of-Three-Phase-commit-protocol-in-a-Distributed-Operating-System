#Name - Mallavarapu Johnsy Vineela
#STudent ID : 1001562621
#Participant program for the Chat Room System
#Please read the inline comments to gain a thorough understanding of the code
#The references / citations for the code built is mentioned in the end of the program

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from _datetime import datetime
import tkinter
import time
import os
import os.path

client_name_list = ["Coord", "Jo", "System", "Professor", "TA", "Johnsy", "Pooja", "God"]
#The recieve message is used to recieve the messages from the server and decode them to insert into the GUI window
#The messages get displayed in the listbox which is the message display area
def receive():
    t_end = time.time() + 120
    global msg
    global prepcnt
    global abcnt
    global state
    prepcnt = 0
    abcnt = 0
#We evaluate until the condition holds true
    while True:
#Sometimes OsError gets thrown because the client exited abruptly so we catch the exception
        try:
#we receive the message sent from the server and as already mentioned, it gets inserted into the application window
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            mlist.insert(tkinter.END,msg)

#When invalid username is input, the server sends exit to the client which in turn calls the on_closing function to quit the window
            if "{exit}" in msg:
                on_closing()

#Once the participant is welcomed to the chatroom, it declares itself to be in INIT state
            if "to the CHATROOM" in msg:
                splitmsg1 = msg.split("!")
                global clientname
                clientname = splitmsg1[1]
                state = "... IN INIT STATE ..."
                mlist.insert(tkinter.END, state)

#The participant sits in INIT state for 10 minutes until it receives vote request from the coordinator.
#If there is no activity going on for 10 minutes, then the participant will abort assuming coordinator ceashed
                roottop.after(60000, aborttemp)

#The filename is created with the name of the client appended to the word 'log'
                filename = "log"+clientname+".txt"
                PATH = './'+filename
                print(PATH)

#This condition checks if the path is accessible and if the file already exisits
                if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
                    print("File exists and is readable")

#If the file exists, then read the file content and display it in the GUI
                    with open(filename, 'r') as f:
                        content = f.read().splitlines()
                        mlist.insert(tkinter.END, content)

#If the filename doesnt exist, then create a new file
                else:
                    with open(filename, 'w'):
                        pass

#If the coordinator sends the vote request for the arbitrary string, we extract the string that needs to be committed
            if "This is the arbitrary string" in msg:
                state = "... IN READY STATE ..."
                mlist.insert(tkinter.END, state)
                splitmsg = msg.split(";")
                global arbitmsg
                arbitmsg = splitmsg[1]
                #print(arbitmsg)

#If Global-commit command is given by the coordinator, the extracted string is now committed to the file.
#The state is changed from PRECOMMIT to COMMIT
#We have a counter to let us know if ever a Global commit was sent by the coordinator
            if "Global-Commit" in msg:
                prepcnt = prepcnt + 1
                print(prepcnt)
                state = "... IN COMMIT STATE ..."
                mlist.insert(tkinter.END, state)
                string = "... TRANSACTION COMMITTED: String written to file ..."
                mlist.insert(tkinter.END, string)
                with open("log"+clientname+".txt",'a') as logfile:
                    logfile.write(arbitmsg + "\n")

#If any abort command is sent by the coordinator (due to timeout or not enough responses as well, the string is not written to the file.
#The state is changed from PRECOMMIT to ABORT
#We have a counter to let us know if ever a Global abort was sent by the coordinator

            if "All participants didn't respond" in msg or "GLOBAL ABORT" in msg or "Global-Abort" in msg:
                abcnt = abcnt + 1
                #print("Abort count is : %d" %abcnt)
                state = "... IN ABORT STATE ..."
                mlist.insert(tkinter.END, state)
                string = "... TRANSACTION NOT COMMITTED: String not written to file ..."
                mlist.insert(tkinter.END, string)
                with open("log"+clientname+".txt", 'w') as logfile:
                    logfile.write("\n")

        except RuntimeError:
            break

        except ConnectionAbortedError:
            break

# Performs the function of sending messages to the server using the send() function of the socket
def send(event=None):
#The message in the text field is received using the get() function
    msg = recvmsg.get()
    tdate = datetime.now()
    msglen = len(msg)
    #print("Raw msg before HTTP: " + msg)

#Sending the recevied message in HTTP format to the server
    http = "HTTP/1.1 " + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    mssg = http + "," + date + "," + msg + "," + server + "," + content

#Clear the input field by setting it to null
    recvmsg.set("")

#The message is then sent to the server for broadcast in bytes format
    client_socket.send(bytes(mssg, "utf8"))

#If the received message is exit, we want the window to close so we give the command roottop.quit()
    if msg == "{exit}":
        roottop.quit()

#The on-closing function is called to handle the closing of the window when the command is received from the user
#The events values are passed by the binders
#The value of the recvmsg is set to exit and further control is transferred to the send function above
def on_closing(event=None):
    recvmsg.set("{exit}")
    send()

#In case the coordinator crashes, the participant checks with the other participants to see if the transaction should be committed
#If the participant responds to commit, then the participant writes the string to the file.
def crashresp(arbitmsg):
    if "PRECOMMIT" in msg or "COMMIT" in msg:
        cabmsg = "Committing!"
        mlist.insert(tkinter.END, cabmsg)
        state = "... MOVING TO COMMIT STATE ..."
        mlist.insert(tkinter.END, state)
        #print(arbitmsg)
        with open("log" + clientname + ".txt", 'a') as logfile:
            logfile.write(arbitmsg + "\n")

#If no response is received before timeout, the transaction gets aborted
    else:
        abmsg = "Aborting!"
        mlist.insert(tkinter.END, abmsg)
        state = "... MOVING TO ABORT STATE ..."
        mlist.insert(tkinter.END, state)
        with open("log" + clientname + ".txt", 'w') as logfile:
            logfile.write("\n")

#When the participant is in the precommit state, once the coordinator sends acknowledgement, participant should also send ack
#The user is prompted at this point to click the ack button for acknowledging
def ack(event=None):
    msg = "ack"
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1" + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content
    client_socket.send(bytes(fullmsg, "utf8"))
    # pmsg = "... ACKNOWLEDGED TRANSACTION ..."
    # mlist.insert(tkinter.END, pmsg)

def commit(event=None):
    msg = "PREPARE-COMMIT"
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1" + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content
    client_socket.send(bytes(fullmsg, "utf8"))

#Once the participant is ready to commit, it goes to the precommit state indicating that it is ready to write to the file.
    state = "... IN PRECOMMIT STATE ..."
    mlist.insert(tkinter.END, state)

#If the ack from the coordinator is not recevied within 2 minutes, the participant assumes that the coordinator has crashed
#We have written a coordcrash function to handle this event.
    roottop.after(120000, coordcrash)

#The coordinator crash function checks if the current state of the participant is prep commit or ready to check with the other participants
#The prepcnt and abcnt is checked to see if they are 0 to ensure coordinator didnt send any vote decision
#It waits for other participants to respond within 30 seconds and calls the crashresp function to handle further
def coordcrash(event=None):
    print(state)
    if "PREPARE-COMMIT" in state or "READY" in state:
        if prepcnt == 0 or abcnt == 0:
            crashmsg = "Coordinator crashed - What is the global state? " + "\n"
            tdate = datetime.now()
            msglen = len(crashmsg)
            http = "HTTP/1.1" + time.ctime()
            date = "Date: " + str(tdate)
            server = "Server: JetBrains Pycharm 2017"
            content = "Content Length: " + str(msglen)
            mssg = http + "," + date + "," + crashmsg + "," + server + "," + content
            client_socket.send(bytes(mssg, "utf8"))

# Wait for 30 seconds to receive responses and then perform manipulations
            roottop.after(30000, crashresp, arbitmsg)

#This function gets executed if the participant sits in the INIT state for more than 5 mins.
#It assumes that the coordinator has crashed and aborts the transaction
def aborttemp(event=None):
    print(state)
    if state == "... IN INIT STATE ...":
        msg = "Timeout - No vote request from coordinator"
        cstate = "IN ABORT STATE"
        mlist.insert(tkinter.END, msg)
        mlist.insert(tkinter.END, cstate)
    else:
        print("No action taken for init timeout")

def abort(event=None):
#The state variable is checked if in init state to affirm that the coordinator has crashed
    if "IN PRECOMMIT STATE" in state:
        pmsg = "... ABORT NOT ALLOWED ..."
        mlist.insert(tkinter.END, pmsg)

    else:
        msg = "ABORT"
        tdate = datetime.now()
        msglen = len(msg)
        http = "HTTP/1.1" + time.ctime()
        date = "Date: " + str(tdate)
        server = "Server: JetBrains Pycharm 2017"
        content = "Content Length: " + str(msglen)
        fullmsg = http + "," + date + "," + msg + "," + server + "," + content
        client_socket.send(bytes(fullmsg, "utf8"))
        pmsg = "... ABORT TRANSACTION ..."
        mlist.insert(tkinter.END, pmsg)



if __name__ == "__main__":

    HOST = 'localhost'
    PORT = 25000

#We set the buffer size to 1024 bytes for receiving and sending messages
    BUFSIZ = 6144

#The ADDR parameter takes the user provided input of Host name and port number to create the socket and connect with the server
    ADDR = (HOST, PORT)

#The client socket is thus created and the connection request is sent using the ADDR paramter
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

#Implementation of TKINTER GUI for the application
#roottop is the object of the TKinter class
    roottop = tkinter.Tk()

#We give the title to display in the title bar of the window
    roottop.title("ChatRoomSystem - Participant")

#Frame is the invisible screen that contains the contents of the window
#We assign it to the window by passing roottop as parameter
    mframe = tkinter.Frame(roottop)

#The received message is then assigned to a variable. This can be called as the TKinter variable
    recvmsg = tkinter.StringVar()

#We then set the text in the text box to the following content
    recvmsg.set("Your messages here.")

#Scrollbar is set to scroll through the past messages if any in the window
    scrollbar = tkinter.Scrollbar(mframe)

#We implement a listbox for and put it inside the frame with the corresponding height and width and set the scrollbar
    mlist = tkinter.Listbox(mframe, height=10, width=80, yscrollcommand=scrollbar.set)

#We pack the widgets into the screen in TKinter in order for them to display on the screen
#We set the scrollbar to the right side of the window and fill parameter makes it extend along with the window in the Y axis
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

#We then pack the list as well similar to above and the BOTH parameter implies that it gros in both X and Y axes
    mlist.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
#    mlist.pack()
    mframe.pack()

#entry_field widget which is the Entry widget is used to allow user to type one line of text
#similar to a textbox and we put it on the window. The recvmsg variable values are displayed here
    entry_field = tkinter.Entry(roottop, textvariable=recvmsg)

#We bind the Return variable to the function to equate the send command
    entry_field.bind("<Return>", send)
    entry_field.pack()

#The send button on the screen is assigned the same functionality as the Return key

#    login_button = tkinter.Button(roottop, text="LOGIN")
#    login_button.pack(fill = tkinter.X)
#    send_button = tkinter.Button(roottop, text="SEND", command=send)
#    send_button.pack()

    commit_button = tkinter.Button(roottop, text="PREPARE-COMMIT", command=commit)
    commit_button.pack(fill = tkinter.X)

    abort_button = tkinter.Button(roottop, text="ABORT", command=abort)
    abort_button.pack(fill = tkinter.X)

    ack_button = tkinter.Button(roottop, text="ACK", command=ack)
    ack_button.pack(fill = tkinter.X)

    exit_button = tkinter.Button(roottop, text="EXIT", command=on_closing)
    exit_button.pack()

#Protocol handler refers to the interaction between application and window
#This protocol decides what needs to be done when the user closes the window directly using the X command on the window
    roottop.protocol("WM_DELETE_WINDOW", on_closing)

#The thread is received here and the receive function is then called for decoding the messages
#Then the thread is started to begin the communication
    receive_thread = Thread(target=receive)
    receive_thread.start()

#The mainloop function is used to ensure the TKinter window remains on the screen until a user action interrupts it
    tkinter.mainloop()




#CITATIONS
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
# https://github.com/Delvison/Muilti-Client-Chatroom
# https://www.youtube.com/watch?v=Iq1dM4-jEX8
# https://stackoverflow.com/questions/26275994/write-line-with-timestampmessage-to-file
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# https://stackoverflow.com/questions/919897/how-to-find-a-thread-id-in-python
# https://www.binarytides.com/code-chat-application-server-client-sockets-python/
# http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
# https://github.com/nnshet/distributed-Systems/blob/master/chatApp
# https://www.youtube.com/watch?v=GZyQmkxH8as
# https://www.youtube.com/watch?v=ZwxTGGEx-1w
# https://github.com/JackZProduction/python_chat
# https://wiki.python.org/moin/TkInter
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# https://stackoverflow.com/questions/10556479/running-a-tkinter-form-in-a-separate-thread/10556698#10556698
# https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop
# https://github.com/idlespork/idlespork/issues/8
# https://stackoverflow.com/questions/26275994/write-line-with-timestampmessage-to-file
# https://stackoverflow.com/questions/33235626/saving-to-msg-file-in-python-or-alternatively-sending-mail-to-the-file-system
# https://pythonspot.com/tk-message-box/
# https://github.com/grisha/mod_python/issues/41
# https://stackoverflow.com/questions/30396709/python-3-encoding-or-errors-without-a-string-argument/30396845#30396845
# https://stackoverflow.com/questions/12607516/python-udp-broadcast-not-sending
# https://github.com/cloudera/impyla/issues/238
# https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
# https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
# https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
# https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
# https://stackoverflow.com/questions/4005796/attributeerror-str-object-has-no-attribute-append
# https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
# https://stackoverflow.com/questions/3752618/python-adding-element-to-list-while-iterating
# https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list
# https://stackoverflow.com/questions/44901806/python-error-message-io-unsupportedoperation-not-readable
# https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist
# https://stackoverflow.com/questions/18406165/creating-a-timer-in-python
# https://stackoverflow.com/questions/21242848/how-to-add-timer-with-start-stop-gui-in-python
#https://stackoverflow.com/questions/25731997/python-while-loop-causes-entire-program-to-crash-in-tkinter
#https://stackoverflow.com/questions/7491777/tkinter-is-freezing-while-the-loop-is-processing-how-can-i-prevent-it
#https://www.daniweb.com/programming/software-development/threads/505937/python-tkinter-delay-hangs-using-after-method