'''
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *

import sys

app = QApplication(sys.argv)

#l = Qlabel("hello")

w = QVideoWidget()
w.show()


player = QMediaPlayer()
#player.setMedia(QMediaContent(QUrl.fromLocalFile("/Users/chasedeslaurier/Downloads/fly.mp4")))
player.setMedia(QMediaContent(QUrl("http://clips.vorwaerts-gmbh.de/VfE_html5.mp4")))
player.setVideoOutput(w)



player.play()

sys.exit(app.exec_())
'''
