import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QFileDialog, QStyle
from PyQt5.QtMultimediaWidgets import QVideoWidget

#QtDesign
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 594)
        MainWindow.setStyleSheet("QMainWindow {background:rgb(206, 206, 206)}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.videoWidget = QVideoWidget(self.centralwidget)
        self.videoWidget.setGeometry(QtCore.QRect(10, 10, 781, 461))
        self.videoWidget.setObjectName("videoWidget")

        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(10, 490, 51, 51))
        self.playButton.setObjectName("playButton")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(70, 490, 51, 51))
        self.openButton.setObjectName("openButton")

        self.controlSlider = QtWidgets.QSlider(self.centralwidget)
        self.controlSlider.setGeometry(QtCore.QRect(140, 500, 561, 22))
        self.controlSlider.setOrientation(QtCore.Qt.Horizontal)
        self.controlSlider.setObjectName("timeSlider")

        self.soundSlider = QtWidgets.QSlider(self.centralwidget)
        self.soundSlider.setGeometry(QtCore.QRect(740, 480, 21, 61))
        self.soundSlider.setOrientation(QtCore.Qt.Vertical)
        self.soundSlider.setObjectName("soundSlider")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Abobus"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        


class MyPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.videoPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoPlayer.setVideoOutput(self.videoWidget)
        self.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoPlayer.durationChanged.connect(self.durationChanged)
        self.videoPlayer.stateChanged.connect(self.statusChanged)

        self.openButton.clicked.connect(self.openFile)

        self.playButton.clicked.connect(self.play)

        self.controlSlider.sliderMoved.connect(self.position)

        self.soundSlider.sliderMoved.connect(self.setVolume)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.videoPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName))) 

    def play(self):
        if self.videoPlayer.state() == QMediaPlayer.PlayingState:
            self.videoPlayer.pause()
        else:
            self.videoPlayer.play()

    def statusChanged(self):
        if self.videoPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position(self, position):
        self.videoPlayer.setPosition(position)

    def positionChanged(self, position):
        self.controlSlider.setValue(position)

    def durationChanged(self, duration): 
        self.controlSlider.setRange(0, duration)

    def setVolume(self, volume):
        self.videoPlayer.setVolume(volume)
        self.statusBar().showMessage(f'Громкость - {volume}%')
    
    


    


    