import sys
import sqlite3

from PyQt5 import QtGui, QtCore
from Design import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QFileDialog, QStyle
from PyQt5.QtWidgets import QApplication
from CreateDataBase import create


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

        self.likeButton.setIcon(QtGui.QIcon('./Images/heart_blank.png'))
        self.likeButton.setIconSize(QtCore.QSize(30, 30))
        self.likeButton.clicked.connect(self.liked)

        self.showButton.clicked.connect(self.showAll)

        self.fileName = ''

    def openFile(self):
        connect = sqlite3.connect("likedbd.sqlite")
        cursor = connect.cursor()

        lines = cursor.execute('SELECT * FROM liked').fetchall()
        names = [''.join(elem) for elem in lines]

        name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            QDir.homePath(),
            "Media (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)",
        )

        if name:
            self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(name)))
            self.fileName = name

            if self.fileName.split(".")[0].split("/")[-1] not in names:
                self.likeButton.setIcon(QtGui.QIcon('./Images/heart_blank.png'))
            else:
                self.likeButton.setIcon(QtGui.QIcon('./Images/heart_filled.png'))

            self.flag = True

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

    def keyPressEvent(self, event):
        if event.key() == 32:
            self.play()
        elif event.key() in (65, 1060):
            position = self.videoPlayer.position() - 5000

            self.videoPlayer.setPosition(position)
            self.controlSlider.setValue(position)
        elif event.key() in (68, 1042):
            position = self.videoPlayer.position() + 5000

            self.videoPlayer.setPosition(position)
            self.controlSlider.setValue(position)
        elif event.key() in (87, 1062):
            volume = self.videoPlayer.volume()

            if self.videoPlayer.volume() != 100:
                volume += 1

            self.soundSlider.setValue(volume)
            self.setVolume(volume)
        elif event.key() in (83, 1067):
            volume = self.videoPlayer.volume()

            if self.videoPlayer.volume() != 0:
                volume -= 1

            self.soundSlider.setValue(volume)
            self.setVolume(volume)
        elif event.key() in (70, 1040):
            self.openFile()

    def wheelEvent(self, event):
        volume = self.videoPlayer.volume()
        if event.angleDelta().y() > 0:
            if volume != 100:
                volume += 1

            self.soundSlider.setValue(volume)
            self.setVolume(volume)
        else:
            if volume != 0:
                volume -= 1

            self.soundSlider.setValue(volume)
            self.setVolume(volume)

    def liked(self):
        if self.fileName:
            if self.flag:
                self.addElem()
                self.flag = False
                self.likeButton.setIcon(QtGui.QIcon('./Images/heart_filled.png'))
            else:
                self.deleteElem()
                self.flag = True
                self.likeButton.setIcon(QtGui.QIcon('./Images/heart_blank.png'))

    def deleteElem(self):
        name = self.fileName.split(".")[0].split("/")[-1]

        if name:
            connect = sqlite3.connect("likedbd.sqlite")
            cursor = connect.cursor()

            cursor.execute(f'DELETE FROM Liked WHERE title = "{name}"')

            connect.commit()
            connect.close()

    def addElem(self):
        name = self.fileName.split(".")[0].split("/")[-1]

        if name:
            connect = sqlite3.connect("likedbd.sqlite")
            cursor = connect.cursor()

            count = len(
                cursor.execute(
                    f'SELECT title FROM Liked WHERE title = "{name}"'
                ).fetchall()
            )

            if count == 0:
                cursor.execute(f'INSERT INTO Liked (title) VALUES ("{name}")')

            connect.commit()
            connect.close()

    def showAll(self):
        connect = sqlite3.connect("likedbd.sqlite")
        cursor = connect.cursor()

        lines = cursor.execute('SELECT * FROM liked').fetchall()
        text = '\n'.join([''.join(elem) for elem in lines])

        message = QMessageBox()
        message.setWindowIcon(QtGui.QIcon('./Images/heart_filled.png'))
        message.setWindowTitle('Понравившееся')
        message.setText(text)
        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPlayer()
    create()
    ex.show()
    sys.exit(app.exec_())
