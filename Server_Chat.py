#Name - Mallavarapu Johnsy Vineela
#Server program for the Chat Room System
#Please read the inline comments to gain a thorough understanding of the code
#The references / citations for the code built is mentioned in the end of the program


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading
from datetime import datetime
from datetime import timedelta
import time
import tkinter


#We declare two dictionaries for storing the information about the clients and the addresses
clients = {}
IPaddresses = {}
currentlist = [""]

#We assign the port variable and host here
HOST = ''

#The port variable is set as a default to 25000
PORT = 25000

#The Buffer size for sending and receiving messages is set to 1024
BUFFERSIZE = 6144

#The hostname and port number recieved is combined to created a socket
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)

#The server is then bound to that host and port number until the socket is closed
SERVER.bind(ADDR)

#We define this function to listen and accept the incoming connection requests from the clients
def acceptconnections():
    try:
        while True:
# Until the condition is true, the client request is accepted and the values are stored in the variables
            client, client_address = SERVER.accept()

#We initialize a global variable called starttime to evaluate the duration of the client's messages
#This is displayed in the window alongside the client name
            global starttime
            starttime = time.time()

#We print in the server console the IP address of the client connected
            print("%s:%s has connected." % client_address)

#Then the server sends a welcome message to be displayed in the TKinter window
            client.send(bytes("Welcome to the CHAT ROOM! Provide your valid username!", "utf8"))

#We store the client address in another variable
            IPaddresses[client] = client_address

#Once all the above are done, a separate thread is created for the client and the control is passed on to the next function.
            Thread(target=work_on_the_client, args=(client,)).start()

#When the server is offline, we get our connection refused so we handle that exception
    except ConnectionRefusedError:
        print("Server Offline")
        clomsg = "Server Offline"
        mlist.insert(tkinter.END, clomsg)


#Now the server talks with the client and the function handles the incoming requests
def work_on_the_client(client):

#We print the thread ID of every single client on the server console
    ThreadID = threading.get_ident()
    #print("Thread with ID %s has been assigned for the new client %s:" % (ThreadID, client))
    accmsg = "Thread with ID %s has been assigned for the new client %s:" % (ThreadID, client)
    mlist.insert(tkinter.END, accmsg)

#The username of the client is received in the HTTP format and decoded
    fullname = client.recv(BUFFERSIZE).decode("utf8")
    splitname = fullname.split(",")
    clientname = splitname[2]
    #print(currentlist)
    if clientname in currentlist:
        clomsg = "Duplicate username"
        mlist.insert(tkinter.END, clomsg)
        clientname = "Invalid"
    else:
        currentlist.append(clientname)
        print(currentlist)
#In order to allow only the valid list of users to access the chat room and also rejecting bad names, we provide a list of valid username
#If the client provides one of the below usernames, it is allowed access
    client_name_list= ["Coord","Jo","System","Professor","TA","Johnsy","Pooja","God"]

#We check if the username is present in one of the valid names list
#for i in client_name_list:
# #If the username is valid, a welcome message is sent to the client window using the send function of the socket
    if clientname in client_name_list:
            welcome = 'Welcome !%s! to the CHATROOM' % clientname
            client.send(bytes(welcome, "utf8"))
            #mlist.insert(tkinter.END, welcome)

    #The message that a new client has joined is then broadcasted to all the clients in the network connected to the server
            msg = "%s has joined the chat!" % clientname
            broadcast(bytes(msg, "utf8"))
            mlist.insert(tkinter.END, msg)

    #We store the client name in the clients dictionary along with the connection information
            clients[client] = clientname

            try:
                while True:
    # #The messages sent to the server are received in the message variable
                    fullmsg = client.recv(BUFFERSIZE).decode("utf-8")
                    serverhttp = "200 OK " + fullmsg
                    mlist.insert(tkinter.END, serverhttp)
                    splitmsg = fullmsg.split(",")
                    msg = splitmsg[2]
                    decmsg = msg
                    msg = bytes(msg, "utf8")

    #We check if the user has provided the message that we wishes to exit the chatroom.
    #Based on the message received, the following loop gets executed
                    if msg != bytes("{exit}", "utf8"):

    #We set a endtime variable to display the difference in time between the entry and first message
                        endtime = time.time()
                        delta = (endtime - starttime)

    #We use the timedelta function to convert the seconds received in the delta variable above to time format
                        deltaf = str(timedelta(seconds=delta))

    #The obtained string in deltaf will have microseconds information as well, so we split the information to the first 4 digits
    #The splitted value is then joined together to be represented as time
                        fdeltaf = ':'.join(str(deltaf).split(':')[:2])

    #The messages are printed on the server console
                        propmsg = clientname + "(" + fdeltaf + "): " + decmsg
                        mlist.insert(tkinter.END, propmsg)

    #The client name and his messages are then broadcasted to all the clients with the following function
                        broadcast(msg, clientname + "(" + fdeltaf + "): ")

    #If the client has closed the window using the X button or thas speicified exit expicitly, the following code gets executed
                    else:
                        client.send(bytes("{exit}", "utf8"))

    #The server console then displays the information regarding the client getting disconnected
                        stime = str(datetime.now().strftime('%H:%M'))
                        print("Client '%s' disconnected @: '%s'" % (clientname, stime))
                        dismsg = "Client '%s' disconnected @: '%s'" % (clientname, stime)
                        mlist.insert(tkinter.END, dismsg)

    #The clients are all informed that the client has exit the chat room
                        broadcast(bytes("%s has left the chat." % clientname, "utf8"))
                        client.close()
                        del clients[client]

    #The client information is then deleted from the dicitionary
            except OSError:
                print("Client Socket closed")
                clomsg = "Client socket closed"
                mlist.insert(tkinter.END, clomsg)
    else:
        try:
            clomsg = "Invalid username"
            mlist.insert(tkinter.END, clomsg)
            client.send(bytes("{exit}", "utf8"))
        #time.sleep(5)
            client.close()

        except OSError:
            print("Client Socket closed")
            clomsg = "Client socket closed"
            mlist.insert(tkinter.END, clomsg)



#This is the broadcase funtion that displays the messages to all the clients connected to the server
#It takes the message and the name of the client as input arguments
def broadcast(msg, prefix=""):

#If the client is present in the client dictionary, we send the data to them
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

#This is the main function of the program which calls all the above functions


if __name__ == "__main__":

#We specify that the server is limited to listen only to 4 clients at a time
    SERVER.listen(4)
    print("...Listening...")

    roottop = tkinter.Tk()
    roottop.title("ChatRoomSystem - Server GUI")
    mframe = tkinter.Frame(roottop)
    scrollbar = tkinter.Scrollbar(mframe)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    mlist = tkinter.Listbox(mframe, height=10, width=150, yscrollcommand=scrollbar.set)
   # mlist = tkinter.Listbox(mframe, height=10, width=80, yscrollcommand=scrollbar1.set)
    mlist.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    lmsg = "Listening..."
    mlist.insert(tkinter.END, lmsg)
    mframe.pack()

#The server accepts the client requests by calling the accept connection function
    ACCEPT_THREAD = Thread(target=acceptconnections)

#Then the thread is started for that client
    ACCEPT_THREAD.start()

    roottop.protocol("WM_DELETE_WINDOW", roottop.quit())
    tkinter.mainloop()

#Join method performs synchronization by blocking the calling thread until the thread whose join is called is completed
    ACCEPT_THREAD.join()

#We then close the server socket and no more connections get accepted
    SERVER.close()


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