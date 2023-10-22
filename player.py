import sys

from design import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QFileDialog, QStyle
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MyPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.videoPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoPlayer.setVideoOutput(self.videoWidget)
        self.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoPlayer.durationChanged.connect(self.durationChanged)
        self.videoPlayer.stateChanged.connect(self.statusChanged)
        self.videoPlayer.setPlaybackRate(1)
        self.videoPlayer.setVolume(20)
        self.statusBar().showMessage(f'Громкость - {20}%')

        self.openButton.clicked.connect(self.openFile)

        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.controlSlider.sliderMoved.connect(self.position)

        self.soundSlider.setValue(20)
        self.soundSlider.sliderMoved.connect(self.setVolume)

        self.speedButton.clicked.connect(self.playbackRate)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())

        if fileName != '':
            self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

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

    def playbackRate(self):
        rateValues = [1.0, 1.25, 1.5, 1.75, 2.0, 0.25, 0.5, 0.75]

        if self.videoPlayer.playbackRate() == 0.75:
            self.videoPlayer.setPlaybackRate(rateValues[0])
        else:
            self.videoPlayer.setPlaybackRate(
                rateValues[rateValues.index(self.videoPlayer.playbackRate()) + 1]
            )

        self.speedButton.setText(str(self.videoPlayer.playbackRate()))
