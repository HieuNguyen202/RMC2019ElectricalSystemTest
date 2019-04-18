from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyle, QStyleOptionSlider
from PyQt5.QtCore import QRect, QPoint, Qt



"""The mainwindow of the GUI"""
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Set up window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("RMC2019 - Electrical Test Program")
        MainWindow.resize(450, 200)

        self.nodes = list()

        #Set up central widget
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)

        #Set up layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(0)
        self.centralWidget.setLayout(self.layout)

        #Setup status bar
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        #Setup menu bar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 614, 22))
        MainWindow.setMenuBar(self.menuBar)

        #Setup tool bar
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.setMaximumHeight(25)
        self.mainToolBar.setMinimumWidth(450)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

        #Set up widgets
        self.lbStatus = QtWidgets.QLabel("No status!")
        self.lbIPAddress = QtWidgets.QLabel("IP Address: ")
        self.txtIPAddress = QtWidgets.QTextEdit("192.168.0.")
        self.lbPort = QtWidgets.QLabel("Port: ")
        self.txtPort = QtWidgets.QTextEdit("2345")
        self.btnConnect = QtWidgets.QPushButton("Connect")
        self.controlModule = ControlWidget()
        self.controlModule.hide()

        self.txtPort.setMinimumWidth(70)
        self.txtPort.setMaximumWidth(70)

        self.txtIPAddress.setMinimumWidth(120)
        self.txtIPAddress.setMaximumWidth(120)

        #Add widgets to menu bar


        #Add widgets to tool bar
        self.mainToolBar.addWidget(self.lbIPAddress)
        self.mainToolBar.addWidget(self.txtIPAddress)
        self.mainToolBar.addWidget(self.lbPort)
        self.mainToolBar.addWidget(self.txtPort)
        self.mainToolBar.addWidget(self.btnConnect)

        #Add widgets to status bar
        self.statusBar.addWidget(self.lbStatus)


        #Add widgets to the layout
        self.layout.addWidget(self.controlModule)

    def appendNode(self):
        n = ControlWidget()
        self.layout.addWidget(n)
        self.nodes.append(n)
        return n

"""Contains controls (buttons, sliders) of a distributed node."""
class ControlWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        #Create button and sliders
        self.btnUp = QtWidgets.QPushButton("Up")
        self.btnDown = QtWidgets.QPushButton("Down")
        self.btnLeft = QtWidgets.QPushButton("Left")
        self.btnRight = QtWidgets.QPushButton("Right")
        self.btnRelease = QtWidgets.QPushButton("Release")
        self.btnReset = QtWidgets.QPushButton("Reset Arduino")
        self.sliderSpeed = LabeledSlider(minimum=0, maximum=100, interval=10, orientation=Qt.Horizontal)

        # self.layout.addWidget(widget, row, column, rowSpan, columnSpan)
        self.layout.addWidget(self.btnUp , 1, 2)
        self.layout.addWidget(self.btnDown , 2, 2)
        self.layout.addWidget(self.btnLeft , 2, 1)
        self.layout.addWidget(self.btnRight , 2, 3)
        self.layout.addWidget(self.btnRelease , 1, 1)
        self.layout.addWidget(self.btnReset , 1, 3)
        self.layout.addWidget(self.sliderSpeed, 3, 1, 1, 3)

"""Source: https://stackoverflow.com/questions/47494305/python-pyqt4-slider-with-tick-labels"""
class LabeledSlider(QtWidgets.QWidget):
    def __init__(self, minimum, maximum, interval=1, orientation=Qt.Horizontal,
            labels=None, parent=None):
        super(LabeledSlider, self).__init__(parent=parent)

        levels=range(minimum, maximum+interval, interval)
        if labels is not None:
            if not isinstance(labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(labels) != len(levels):
                raise Exception("Size of <labels> doesn't match levels.")
            self.levels=list(zip(levels,labels))
        else:
            self.levels=list(zip(levels,map(str,levels)))

        if orientation==Qt.Horizontal:
            self.layout=QtWidgets.QVBoxLayout(self)
        elif orientation==Qt.Vertical:
            self.layout=QtWidgets.QHBoxLayout(self)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin=10
        self.top_margin=10
        self.right_margin=10
        self.bottom_margin=10

        self.layout.setContentsMargins(self.left_margin,self.top_margin,
                self.right_margin,self.bottom_margin)

        self.sl=QtWidgets.QSlider(orientation, self)
        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)
        if orientation==Qt.Horizontal:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sl.setMinimumWidth(300) # just to make it easier to read
        else:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksLeft)
            self.sl.setMinimumHeight(300) # just to make it easier to read
        self.sl.setTickInterval(interval)
        self.sl.setSingleStep(1)

        self.layout.addWidget(self.sl)

    def paintEvent(self, e):

        super(LabeledSlider,self).paintEvent(e)

        style=self.sl.style()
        painter=QPainter(self)
        st_slider=QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation=self.sl.orientation()

        length=style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.sl)
        available=style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:

            # get the size of the label
            rect=painter.drawText(QRect(), Qt.TextDontPrint, v_str)

            if self.sl.orientation()==Qt.Horizontal:
                # I assume the offset is half the length of slider, therefore
                # + length//2
                x_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available)+length//2

                # left bound of the text = center - half of text width + L_margin
                left=x_loc-rect.width()//2+self.left_margin
                bottom=self.rect().bottom()

                # enlarge margins if clipping
                if v==self.sl.minimum():
                    if left<=0:
                        self.left_margin=rect.width()//2-x_loc
                    if self.bottom_margin<=rect.height():
                        self.bottom_margin=rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

                if v==self.sl.maximum() and rect.width()//2>=self.right_margin:
                    self.right_margin=rect.width()//2
                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

            else:
                y_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available, upsideDown=True)

                bottom=y_loc+length//2+rect.height()//2+self.top_margin-3
                # there is a 3 px offset that I can't attribute to any metric

                left=self.left_margin-rect.width()
                if left<=0:
                    self.left_margin=rect.width()+2
                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

            pos=QPoint(left, bottom)
            painter.drawText(pos, v_str)

        return

if __name__ == '__main__':
    app = QtGui.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()