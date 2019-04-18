#!/usr/bin/python3
from interface import *
from PyQt5.QtCore import QCoreApplication, QTimer

from serial import Serial
import signal

server = None
nodes = list()
arduino = Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)

def startListening():
    global server
    server = Server(port=2345)
    server.newClient.connect(appendNewClient)

def appendNewClient(client):
    global nodes, arduino
    node = CLINode(client, arduino)
    print("New connection from: ", client.peerAddress().toString(), 'port', client.peerPort())
    nodes.append(node)

#Support Control+C
# Call this function in your main after creating the QApplication
def setup_interrupt_handling():
    """Setup handling of KeyboardInterrupt (Ctrl-C) for PyQt."""
    signal.signal(signal.SIGINT, _interrupt_handler)
    # Regularly run some (any) python code, so the signal handler gets a
    # chance to be executed:
    safe_timer(50, lambda: None)
def _interrupt_handler(signum, frame):
    """Handle KeyboardInterrupt: quit application."""
    QCoreApplication.quit()
def safe_timer(timeout, func, *args, **kwargs):
    """
    Create a timer that is safe against garbage collection and overlapping
    calls. See: http://ralsina.me/weblog/posts/BB974.html
    """
    def timer_event():
        try:
            func(*args, **kwargs)
        finally:
            QTimer.singleShot(timeout, timer_event)
    QTimer.singleShot(timeout, timer_event)

if __name__ == '__main__':
    print("Running server.py")
    import sys
    app = QCoreApplication(sys.argv)
    setup_interrupt_handling()
    startListening()
    app.exec_()