#!/usr/bin/python3
from interface import *
from graphics import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
client = None
ui = None

def connectToServer(ip, port):
    global client, ui

    if ui.btnConnect.text() == 'Disconnect':
        client.disconnect()
        return

    client = Client()
    client.connected.connect(connectSignals)
    client.connected.connect(ui.controlModule.show)
    client.connected.connect(lambda: ui.lbStatus.setText("Connected"))
    client.connected.connect(lambda: ui.btnConnect.setText("Disconnect"))

    client.error.connect(lambda: ui.lbStatus.setText("Error"))

    client.disconnected.connect(disconencSignals)
    client.disconnected.connect(ui.controlModule.hide)
    client.disconnected.connect(lambda: ui.lbStatus.setText("Disconnected"))
    client.disconnected.connect(lambda: ui.btnConnect.setText("Connect"))

    if not client.connect(ipAddress=ip, port=port):
        #Disconnect signals
        client.disconnected.connect(lambda: ui.lbStatus.setText("Failed"))
        client.connected.disconnect()
        client.disconnected.disconnect()
        client.error.disconnect()
        return

def connectSignals():
    global ui, client
    ui.controlModule.btnUp.pressed.connect(lambda: client.send(CMD_FORWARD, ui.controlModule.sliderSpeed.sl.value(), 0))
    ui.controlModule.btnDown.pressed.connect(lambda: client.send(CMD_BACKWARD, ui.controlModule.sliderSpeed.sl.value(), 0))
    ui.controlModule.btnLeft.pressed.connect(lambda: client.send(CMD_LEFT, ui.controlModule.sliderSpeed.sl.value(), 0))
    ui.controlModule.btnRight.pressed.connect(lambda: client.send(CMD_RIGHT, ui.controlModule.sliderSpeed.sl.value(), 0))
    ui.controlModule.btnRelease.pressed.connect(lambda: client.send(CMD_RELEASE_MOTORS, 0, 0))
    ui.controlModule.btnReset.pressed.connect(lambda: client.send(CMD_RESET_ARDUINO, 0, 0))

    #Release = speed is zero
    ui.controlModule.btnUp.released.connect(lambda: client.send(CMD_FORWARD, 0, 0))
    ui.controlModule.btnDown.released.connect(lambda: client.send(CMD_FORWARD, 0, 0))
    ui.controlModule.btnLeft.released.connect(lambda: client.send(CMD_FORWARD, 0, 0))
    ui.controlModule.btnRight.released.connect(lambda: client.send(CMD_FORWARD, 0, 0))

def disconencSignals():
    ui.controlModule.btnUp.pressed.disconnect()
    ui.controlModule.btnDown.pressed.disconnect()
    ui.controlModule.btnLeft.pressed.disconnect()
    ui.controlModule.btnRight.pressed.disconnect()
    ui.controlModule.btnRelease.pressed.disconnect()
    ui.controlModule.btnReset.pressed.disconnect()

def setupSignal():
    global ui
    ui.btnConnect.pressed.connect(lambda: connectToServer(ip=ui.txtIPAddress.toPlainText(),
                                                          port=int(ui.txtPort.toPlainText())))

if __name__ == '__main__':
    print("Running client.py")
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    setupSignal()
    MainWindow.show()
    sys.exit(app.exec_())