from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket, QNetworkInterface, QAbstractSocket
from PyQt5.QtCore import pyqtSignal, QObject
import struct

MESSAGE_FORMAT = "Bbb"
MESSAGE_LENGTH = len(MESSAGE_FORMAT)
CMD_FORWARD = 0
CMD_BACKWARD = 1
CMD_LEFT = 2
CMD_RIGHT = 3
CMD_STOP = 4
CMD_RELEASE_MOTORS = 5
CMD_RESET_ARDUINO = 6

"""Get the IP address of the host computer."""
def getIPAddress():
    for ipAddress in QNetworkInterface.allAddresses():
        if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
            break
    else:
        ipAddress = QHostAddress(QHostAddress.LocalHost)
    return ipAddress.toString()

"""Represent the central node. accept and process TCP request from distributed nodes."""
class Server(QTcpServer):
    newClient = pyqtSignal(QTcpSocket)
    def __init__(self, port):
        super(Server, self).__init__()
        self.newConnection.connect(self.acceptConnection)
        self.acceptError.connect(self.acceptErrorHandler)
        if not self.listen(address=QHostAddress.Any, port=port):
            print("interface.py: Unable to start the server: ", self.errorString())
            return
        ipAddress = getIPAddress()
        print('interface.py: The server is running on', ipAddress, 'port', self.serverPort())

    def acceptConnection(self):
        self.newClient.emit(self.nextPendingConnection())

    def acceptErrorHandler(self, socketError):
        print("interface.py: Server accept error", socketError)

"""Represent a distributed node. Contains interfaces to interact with the distributed nodes."""
class Node(QObject):
    newMessage = pyqtSignal(bytes)
    def __init__(self, tcpClient, serial):
        super(Node, self).__init__()
        self.tcpClient = None   #will be set in attach()
        self.attach(tcpClient)
        self.serial = serial

    '''Methods to be used by the the child classes'''
    def attach(self, tcpClient):
        if self.tcpClient != None:
            self.detach()
        tcpClient.readyRead.connect(self.receiveMessage)
        tcpClient.error.connect(self.socketError)
        tcpClient.error.connect(self.detach)
        self.tcpClient = tcpClient
        self.tcpClientAttached()

    #Detach the tcpClient from the Node
    def detach(self):
        self.tcpClient.readyRead.disconnect(self.receiveMessage)
        self.tcpClient.error.disconnect(self.socketError)
        self.tcpClient.error.disconnect(self.detach)
        self.tcpClientDetached()
        self.tcpClient = None


    def write(self, command, value1, value2):
        self.tcpClient.write(struct.pack("Bbb", command.value, value1, value2))

    def receiveMessage(self):
        while self.tcpClient.bytesAvailable() >= MESSAGE_LENGTH:
            raw = self.tcpClient.read(MESSAGE_LENGTH)
            self.serial.write(raw)
            self.newMessage.emit(raw)

    def tcpClientAttached(self):
        print("Need to implement tcpClientAttached")

    def tcpClientDetached(self):
        print("Need to implement tcpClientDetached")

    def socketError(self, status):
        print("Need to implement connectionError")

"""An Node implementation that is used in a command line interface. Used in computer with no graphics"""
class CLINode(Node):
    def __init__(self, tcpClient, serial):
        super(CLINode, self).__init__(tcpClient, serial)
        self.newMessage.connect(self.newMessageHanlder)

    def newMessageHanlder(self, raw):
        message = struct.unpack(MESSAGE_FORMAT, raw)
        command = message[0]
        value1 = message[1]
        value2 = message[2]
        print('New message:', command, value1, value2)

    def tcpClientAttached(self):
        print(self.tcpClient.peerAddress().toString()+": tcpClientAttached().")

    def tcpClientDetached(self):
        print(self.tcpClient.peerAddress().toString()+": tcpClientDetached().")

    def socketError(self, status):
        print(self.tcpClient.peerAddress().toString()+": setSharePos(",status,").")

class Client(QTcpSocket):
    def __init__(self):
        super(QTcpSocket, self).__init__()
        self.connected.connect(lambda: print("Connected to server!"))
        self.disconnected.connect(lambda: print("Disconnected from server!"))
        self.readyRead.connect(self.receiveMessage)
        self.error.connect(self.displayError)

    def receiveMessage(self):
        while self.bytesAvailable() >= MESSAGE_LENGTH:
            raw = self.read(MESSAGE_LENGTH)
            print("New message:", struct.unpack(MESSAGE_FORMAT, raw))
            self.newMessage.emit(raw)

    def connect(self, ipAddress, port):
        self.connectToHost(ipAddress, port)
        return self.waitForConnected(1000)

    def disconnect(self):
        self.abort()
        self.close()

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QAbstractSocket.HostNotFoundError:
            print("Client:  The host was not found. Please check the host name and port settings.")
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            print("Client: The connection was refused by the peer. Make sure the fortune server is running, and check that the host name and port settings are correct.")
        else:
            print(self, "Robot Client The following error occurred: ", self.errorString())

    def send(self, command, value1, value2):
        self.write(struct.pack(MESSAGE_FORMAT, command, value1, value2))

