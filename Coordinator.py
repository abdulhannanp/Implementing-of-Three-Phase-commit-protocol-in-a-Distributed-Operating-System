#Name - Mallavarapu Johnsy Vineela
#Coordinator program for the Chat Room System
#Please read the inline comments to gain a thorough understanding of the code
#The references / citations for the code built is mentioned in the end of the program

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from _datetime import datetime
from tkinter import messagebox
from threading import Timer
from datetime import datetime, timedelta
#from Server_Chat import clients
import tkinter
import time

#The recieve message is used to recieve the messages from the server and decode them to insert into the GUI window
#The messages get displayed in the listbox which is the message display area
def receive():
    global messlist
    global abcnt
    global cocnt
    global ackcnt
    messlist = []
    abcnt = 0
    cocnt = 0
    ackcnt = 0
#We evaluate until the condition holds true
    while True:
#Sometimes OsError gets thrown because the client exited abruptly so we catch the exception
        try:
#we receive the message sent from the server and as already mentioned, it gets inserted into the application window
            global rmsg
            rmsg = client_socket.recv(BUFSIZ).decode("utf8")
            mlist.insert(tkinter.END,rmsg)
            print(rmsg)

            if "to the CHATROOM" in rmsg:
                global state
                state = "... IN INIT state ..."
                mlist.insert(tkinter.END, state)

            if "ack" in rmsg:
                ackcnt = ackcnt + 1

            if "ABORT" in rmsg:
                messlist.append(rmsg + ',')
                print(messlist)
                abcnt = abcnt + 1

            if "PREPARE-COMMIT" in rmsg:
                messlist.append(rmsg + ',')
                print(messlist)
                cocnt = cocnt + 1

            #if ackcnt == 3:
            #    committemp()
            #    break

        except RuntimeError:
            break


# Performs the function of sending messages to the server using the send() function of the socket
def send(event=None):
#The message is received using the get() function
    msg = recvmsg.get()
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1 200 OK " + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content
    recvmsg.set("")
    print(fullmsg)

#The received message is then sent to the server for broadcast and to take action
    client_socket.send(bytes(fullmsg, "utf8"))

#If the received message is equal to exit, we want the window to close so we give the command quit()
    if msg == "{exit}":
        roottop.quit()

#The on-closing function is called to handle the closing of the window when the command is received from the user
#The events values are passed by the binders
def on_closing(event=None):
#The value of the recvmsg is set to exit and further control is transferred to the send function above
    recvmsg.set("{exit}")
#Call to the send function
    send()

def aborttemp(event=None):
    state = "... IN ABORT STATE ..."
    mlist.insert(tkinter.END, state)
    msg = "Global-Abort"
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1 200 OK " + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content
    client_socket.send(bytes(fullmsg, "utf8"))

def committemp(event=None):
    #commitmsg = ".... Participants chose prepare-commit and acknowledged ...."
    #mlist.insert(tkinter.END, commitmsg)
    state = ".... COMMIT TRANSACTION ...."
    mlist.insert(tkinter.END, state)
    msg = "Global-Commit"
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1 200 OK " + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content
    client_socket.send(bytes(fullmsg, "utf8"))

def request(event=None):
    armsg = recvmsg.get()
    state = "....IN WAIT STATE...."
    mlist.insert(tkinter.END, state)
#The coordinator waits for 5 minutes until the participants respond.
#If no response is received, it will assume that all the participants have crashed and abort transaction.
#Send the arbitrary string that is received from the text box to the server in HTTP format for broadcast
    msg = "This is the arbitrary string; " + armsg
    tdate = datetime.now()
    msglen = len(msg)
    http = "HTTP/1.1" + time.ctime()
    date = "Date: " + str(tdate)
    server = "Server: JetBrains Pycharm 2017"
    content = "Content Length: " + str(msglen)
    #time.sleep(5)
    fullmsg = http + "," + date + "," + msg + "," + server + "," + content

#Clear the text field
    recvmsg.set("")

#Send the arbitrary string to the server for broadcast
    client_socket.send(bytes(fullmsg, "utf8"))

#Wait for 30 seconds to receive responses and then perform manipulations
    roottop.after(30000, manip_resp)

#Based on the responses recevied, we are going to multicast abort or commit message
#If all the participants have responded, based on the aborts and commits received, the decisions are taken according to 3PC
def manip_resp():
    # lmsg = "No. of responses received are"
    # lcnt = len(messlist)
    # mlist.insert(tkinter.END, lmsg)
    # mlist.insert(tkinter.END, lcnt)
    # pmesss = "The responses received are.."
    # mlist.insert(tkinter.END, pmesss)
    # mlist.insert(tkinter.END, messlist)
    # acnt = "ABORT COUNT: %d" % abcnt
    # ccnt = "COMMIT COUNT: %d" % cocnt
    # mlist.insert(tkinter.END, acnt)
    # mlist.insert(tkinter.END, ccnt)

    if len(messlist) == 3:
        if abcnt > 0:
            aborttemp()

        if cocnt == 3:
            state = "....IN PRECOMMIT STATE...."
            mlist.insert(tkinter.END, state)
            commsg = "ACKNOWLEDGED - Click ACK"
            tdate = datetime.now()
            msglen = len(commsg)
            http = "HTTP/1.1" + time.ctime()
            date = "Date: " + str(tdate)
            server = "Server: JetBrains Pycharm 2017"
            content = "Content Length: " + str(msglen)
            fullmsg = http + "," + date + "," + commsg + "," + server + "," + content
            client_socket.send(bytes(fullmsg, "utf8"))

#Wait for half a minute to receive acknowledgements from participants and call the ackfunc to deal with the responses
            roottop.after(30000, ackfunc)

#If the no. of responses received is less than 3 but atleast one is received, we abort the transaction since not enough responses
#The state is moved to ABORT
#Send the message to the server for multicasting to the participants
    if len(messlist) < 3 and len(messlist) > 0:
        abomsg = "Not all participants responded - GLOBAL ABORT"
        state = ".... ABORT TRANSACTION...."
        mlist.insert(tkinter.END, state)
        mlist.insert(tkinter.END, abomsg)
        tdate = datetime.now()
        msglen = len(abomsg)
        http = "HTTP/1.1 " + time.ctime()
        date = "Date: " + str(tdate)
        server = "Server: JetBrains Pycharm 2017"
        content = "Content Length: " + str(msglen)
        fullmsg = http + "," + date + "," + abomsg + "," + server + "," + content
        client_socket.send(bytes(fullmsg, "utf8"))

#If no responses were recieved within the 30 secs time frame, then the coordinator assumes the participants have crashed
#It moves to the abort state and cascades it globally
    if len(messlist) == 0:
        state = "... GOING TO ABORT STATE - Participants crashed ..."
        mlist.insert(tkinter.END, state)
        msg = "Global-Abort"
        tdate = datetime.now()
        msglen = len(msg)
        http = "HTTP/1.1" + time.ctime()
        date = "Date: " + str(tdate)
        server = "Server: JetBrains Pycharm 2017"
        content = "Content Length: " + str(msglen)
        fullmsg = http + "," + date + "," + msg + "," + server + "," + content
        client_socket.send(bytes(fullmsg, "utf8"))

#This function handles the ack messages received from the participants
#If 3 responses were recevied, it multicasts a global commit
#If not, since it knows that the participants all precommited, it still multicasts a global commit - ACC to 3 PC
def ackfunc(event=None):
    if ackcnt == 3:
        amsg = "... All participants have acknowledged ..."
        mlist.insert(tkinter.END, amsg)
        committemp()

    if ackcnt > 0 and ackcnt < 3:
        ackmsg = "One of the participants crashed before acknowledging - Go ahead with commit"
        mlist.insert(tkinter.END, ackmsg)
        committemp()


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
    roottop.title("Co-ordinator GUI")

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
    mlist = tkinter.Listbox(mframe, height=15, width=80, yscrollcommand=scrollbar.set)

#We pack the widgets into the screen in TKinter in order for them to display on the screen
#We set the scrollbar to the right side of the window and fill parameter makes it extend along with the window in the Y axis
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

#We then pack the list as well similar to above and the BOTH parameter implies that it gros in both X and Y axes
    mlist.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    mframe.pack()

#entry_field widget which is the Entry widget is used to allow user to type one line of text
#similar to a textbox and we put it on the window. The recvmsg variable values are displayed here
    entry_field = tkinter.Entry(roottop, textvariable=recvmsg)

#We bind the Return variable to the function to equate the send command
    entry_field.bind("<Return>", send)
    entry_field.pack()

#The send button on the screen is assigned the same functionality as the Return key
    send_button = tkinter.Button(roottop, text="SEND", command=send)
    send_button.pack()

#The exit button transfers the control to the on_closing function and closes the window
    exit_button = tkinter.Button(roottop, text="EXIT", command=on_closing)
    exit_button.pack()

#The req button sends the arbitrary message to the participants and waits for 30 seconds to take further action
    req_button = tkinter.Button(roottop, text="REQUEST", command=request)
    req_button.pack()

#Protocol handler refers to the interaction between application and window
#This protocol decides what needs to be done when the user closes the window directly using the X command on the window
    roottop.protocol("WM_DELETE_WINDOW", on_closing)

#The thread is received here and the receive function is then called for decoding the messages
#Then the thread is started to begin the communication
    receive_thread = Thread(target=receive)
    receive_thread.start()

#   manip_thread = Thread(target=receive_temp)
#   manip_thread.start()

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
#
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