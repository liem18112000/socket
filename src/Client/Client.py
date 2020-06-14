import socket
from ClientUI import UI


class Client:

    def __init__(self):

        # Global data
        self.host = 'localhost'
        self.port = 8000
        self.mySocket = None

        # Flag
        self.QUIT = False

        self.ui = UI()

    # Create a socket
    def createSocket(self):

        try:
            print('Create socket')
            self.mySocket = socket.socket()
            return self.mySocket
        except socket.error as msg:
            print('Socket create error : ' + str(msg))
            return -1

    # Binding socket and listen for connection
    def connectSocket(self):

        print('Connect port : ' + str(self.port))

        # Connect
        try:
            self.mySocket.connect((self.host, self.port))
        except socket.error as msg:
            print('Socket connection error : ' + str(msg))
            return -1

        return 0

    # Client operation
    def clientOperation(self):
        while True:
            # Client talk to server
            flag = self.sendMessage()
            if flag == -1:
                self.QUIT = True
                return flag

            # Client listen for message
            flag = self.receiveMessage()
            if flag == -1:
                self.QUIT = True
                return flag

    # Send messages
    def sendMessage(self):

        msg = self.businessTransactSelect()

        # Send message
        try:
            self.mySocket.send(str.encode(msg))
        except socket.error as msg:
            print('Socket send error : ' + str(msg))
            return -1

        # Check end
        if self.QUIT:
            print('Quit...')
            return -1

        return 0

    # Business transaction
    def businessTransactSelect(self):

        self.ui = UI()

        self.ui.getClientData()

        self.ui.run()

        data = self.ui.clientData

        return data

    # Dispatch received message
    def dispatchMessage(self, message):
        if len(message.decode('utf-8')) > 0:
            print('Receive message : ' + message.decode("utf-8"))
            self.ui = UI()
            self.ui.getServerResponse(message.decode('utf-8').lower())
            self.ui.run()
            message = self.ui.message
            if message == 'quit':
                return -1
        return 0

    # Receive Message
    def receiveMessage(self):
        try:
            message = self.mySocket.recv(1024)
        except socket.error as msg:
            print('Socket receive error : ' + str(msg))
            return -1

        return self.dispatchMessage(message)

    # Get server host from keyboard
    def getServerHost(self):
        self.ui.getServerHost()
        self.ui.run()
        self.host = self.ui.host
        print(self.host)

    # Main Operation
    def run(self):
        # Create Socket
        self.mySocket = self.createSocket()
        if self.mySocket == -1:
            return self.mySocket

        self.getServerHost()

        # Connect Socket
        flag = self.connectSocket()
        if flag == -1:
            return flag

        flag = self.clientOperation()
        if flag == -1:
            return flag


client = Client()
client.run()
