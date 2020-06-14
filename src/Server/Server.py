import socket
from db import Database
import sys
import os
import subprocess
import threading
import time
from queue import Queue

# CMD Command
CMD = {
    'list-client': [
        'list client',
        'list-client',
        'list_client',
        'list',
        'l'
    ],
    'select-client': [
        'select',
    ],
    'help': [
        'help',
        'h'
    ],
    'quit': [
        'q',
        'quit'
    ]
}


class Server:
    def __init__(self):

        # Global Variables
        self.allConnections = []
        self.allAddresses = []
        self.currentActiveClient = None
        self.currentActiveAddress = None
        self.mySocket = None
        self.host = 'localhost'
        self.port = 8000
        self.QUIT = False

        # Declare flag for received data
        self.TEXT_DATA = 2
        selfCMD_DATA = 3

        # Error flag
        self.CLIENT_QUIT_FLAG = 4
        self.INVALID_CLIENT_ID = 5

        # Transact flag
        self.SUCCESS_TRANSACT = 8
        self.WRONG_DATA = 6
        self.OVERFLOW_DATA = 7

        # Jobs
        self.JOB_NUMBER = [1, 2, 3]
        self.NUMBER_OF_THREADS = len(self.JOB_NUMBER)
        self.queue = Queue()

        # CMD Command
        self.CMD = {
            'list-client': [
                'list client',
                'list-client',
                'list_client',
                'list',
                'l'
            ],
            'select-client': [
                'select',
            ],
            'help': [
                'help',
                'h'
            ],
            'quit': [
                'q',
                'quit'
            ]
        }

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
    def bindSocket(self):
        try:
            print('Binding port : ' + str(self.port))

            # Number of maximum bad connections
            badConnection = 5

            # Binding
            self.mySocket.bind((self.host, self.port))

            # Listen
            self.mySocket.listen(badConnection)
            print('Listen...')

        except socket.error as msg:
            print('Socket binding error : ' + str(msg) + '\n' + 'Retrying...')
            self.bindSocket()

    # 1st Thread function:
    # Handling connections from multiple clients
    # Closing previous connections when server restart
    def acceptSocket(self):
        # Close connections
        for connection in self.allConnections:
            connection.close()

        # Delete all
        del self.allConnections[:]
        del self.allAddresses[:]

        # Accept connections
        while True:
            try:
                # Get connection & address
                conn, address = self.mySocket.accept()

                # Prevent timeout
                self.mySocket.setblocking(1)

                # Add connection & address
                self.allConnections.append(conn)
                self.allAddresses.append(address)

                # Inform success accept
                print('Connection has been establish : ')
                print('IP : ' + address[0])
                print('Port : ' + str(address[1]))

            except socket.error as msg:
                print('Socket accept error : ' + str(msg))
                return -1

    # 2nd Thread function:
    # - See all clients
    # - Select a client
    # - Communicate (Send + Receive messages)
    @staticmethod
    def isClientActive(connection):
        try:
            connection.send(str.encode(""))
            return True
        except socket.error:
            return False

    def listClients(self):
        result = ''
        for i, connection in enumerate(self.allConnections):
            if self.isClientActive(connection):
                result = result + str(i) + " => " + str(self.allAddresses[i][0]) + ':' \
                         + str(self.allAddresses[i][1]) + "\n"
            else:
                if not self.removeClient(i):
                    print('Remove client error')
                    return -1
                else:
                    continue

        return result

    def removeClient(self, index):
        try:
            print('Remove connection - ' + self.allAddresses[index][0] + ':' + self.allAddresses[index][1])
            del self.allConnections[index]
            del self.allAddresses[index]
            return True
        except:
            return False
    # ========================================

    # Choose Client
    def selectClient(self, index):

        # Check valid client ID
        if index < 0 or index >= len(self.allConnections):
            print('Client id is invalid! Please choose client from here : ')
            self.listClients()
            return self.INVALID_CLIENT_ID, None

        # Check connection is active
        if not self.isClientActive(self.allConnections[index]):
            self.removeClient(index)
            print('Select client fail!')
            return -1

        # Inform success
        print('Select client ' + str(index) + " - " +
              str(self.allAddresses[index][0]) + ':' + str(self.allAddresses[index][1]))

        # Set selected client to current client
        self.currentActiveClient = self.allConnections[index]
        self.currentActiveAddress = self.allAddresses[index]

        # Return client
        return self.currentActiveClient, self.currentActiveAddress

    # Deselect client
    def deselectClient(self):
        self.currentActiveClient = None
        self.currentActiveAddress = None

    # Send message to client
    def sendMessage(self, conn, address, message):

        print(str(address[0]) + ":" + str(address[1]) + '>send : ' + str(message))

        try:
            conn.send(str.encode(str(message)))
        except socket.error as msg:
            print('Socket send error : ' + str(msg))
            return -1

        return 0

    # Receive message
    def receiveMessage(self, conn, address):
        try:
            message = conn.recv(1024)

        except socket.error as msg:
            print('Socket receive error : ' + str(msg))
            return -1, -1

        return self.dispatchMessage(address, message)

    # Dispatch message
    def dispatchMessage(self, address, message):
        print(str(address[0]) + ':' + str(address[1]) + ">Receive : " + message.decode('utf-8'))
        if message.decode().lower() == 'quit' or message.decode().lower() == '':
            return self.CLIENT_QUIT_FLAG, -1
        else:
            return self.businessTransact(message.decode('utf-8'))

    # Business transact
    def businessTransact(self, message):

        # Output
        output = ""

        # Split data
        clientData = message.split()
        print(clientData)

        # Get data
        db = Database()

        sql = (
            "SELECT route, ticket_type, quantity, price FROM ticket "
            "WHERE route = '" + str(clientData[0]) + "' and ticket_type = '" + str(clientData[1]) + "'"
        )

        for (route, ticket_type, quantity, price) in db.getData(sql):
            print(str(route) + " " + str(ticket_type) + " " + str(quantity) + " " + str(price))

            # Check ticket remain
            if int(clientData[2]) > int(quantity):
                return self.OVERFLOW_DATA, 'Chi con lai ' + str(quantity) + ' ve'

            # Calculate price
            output = 'So tien thanh toan : ' + str(int(clientData[2]) * price)

            # Update data
            sql = (
                "UPDATE ticket set quantity = quantity - " + str(clientData[2]) + " "
                "WHERE route = '" + str(clientData[0]) + "' and ticket_type = '" + str(clientData[1]) + "'"
            )

            db.execute(sql)

        return self.SUCCESS_TRANSACT, output

    # Server main operation
    def serverOperate(self):

        # Start main loop
        while True:
            # Get cmd
            cmd = input('command>')

            # Execute Command in Server
            if cmd.lower() in CMD['list-client']:

                # List all clients
                result = self.listClients()

                # Show list of clients
                print('======== List of Clients ========')
                print(result)

            elif cmd.lower() in CMD['help']:

                # Show list of commands
                print('======== List of commands ========')
                print(CMD)
                print('======== List of commands ========')

            elif cmd.lower() in CMD['quit']:
                print('Quit...')
                QUIT = True
                return -1

            else:
                # Command is not recognize
                print('Command is not recognize. Please type "help" or "h" to see all commands')

    # Server operation
    def clientOperation(self, address, conn):
        output = 0
        while True:
            flag, output = self.receiveMessage(conn, address)
            if flag == self.CLIENT_QUIT_FLAG:
                print('Client go offline')
                break
            elif flag == -1:
                break

            flag = self.sendMessage(conn, address, output)
            if flag == -1:
                break
        return 0

    # Create worker threads
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    # Do next job that is in the queue (handle connections, send commands)
    def work(self):

        while not self.QUIT:

            workID = self.queue.get()

            if workID == 1:
                mySocket = self.createSocket()
                self.bindSocket()
                self.acceptSocket()

            elif workID == 2:
                time.sleep(1.5)
                self.serverOperate()

            elif workID == 3:

                while True:
                    time.sleep(1)
                    for index in range(len(self.allConnections)):

                        # Get client
                        conn, address = self.selectClient(index)

                        # Handle exceptions
                        if conn == -1:
                            return conn
                        elif conn == self.INVALID_CLIENT_ID:
                            continue

                        # Start operate
                        if self.isClientActive(conn):
                            self.clientOperation(address, conn)
                        else:
                            if not self.removeClient(index):
                                print('Remove client error')
                                return -1

            self.queue.task_done()

    # Create jobs
    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)

        self.queue.join()

    # Run
    def run(self):
        self.create_workers()
        self.create_jobs()


server = Server()
server.run()

