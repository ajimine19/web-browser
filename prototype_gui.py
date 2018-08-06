'''
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPixmap
import ssl
import urllib.request
import getHTTPS

class BrowserWindow(QtWidgets.QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        centralWidget = QtWidgets.QWidget(self)
        self.setWindowTitle("Prototype GUI")
        self.setGeometry(100, 100, 200, 200)
        self.setCentralWidget(centralWidget)

        # Set up for overriding the resize event
        #self.resized.connect(self.foo)

        self.vbox = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(self.vbox)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLoad1 = QtWidgets.QPushButton("Load")
        buttonLoad1.clicked.connect(self.setBrowserPage)
        buttonLayout.addWidget(buttonLoad1)
        self.vbox.addLayout(buttonLayout)
        #self.vbox.addStretch()

        # When the linkActivated signal is emitted, it passes
        # the url as a string to the called method.
        hyperlinkLabel = QtWidgets.QLabel()
        hyperlinkLabel.setText('<a href="www.google.com">This is a link</a>')
        hyperlinkLabel.linkActivated.connect(self.linkClicked)
        self.vbox.addWidget(hyperlinkLabel)

        self.numClicks = 0
        self.browserPage = None
        #self.setBrowserPage()
        self.showImage()
        #self.showPage()
        self.show()

        """
        #test RenderObject.getWidget
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()


        url = "https://i.ytimg.com/vi/n8us60ow3iM/maxresdefault.jpg"
        renderO = RenderImage()
        label = QLabel(self)
        #label.setPixmap(renderO.getWidget(url))

        self.resize(500,500)
        self.show()
        """

    def showPage(self):
        url = "http://faculty.up.edu/oster"
        result = getHTTPS.tryGetHTMLSource(url)

        label = QtWidgets.QLabel(result.HTMLSource)
        self.vbox.addWidget(label)

    def showImage(self):
        #url = "https://i.ytimg.com/vi/n8us60ow3iM/maxresdefault.jpg"
        url = "https://yt3.ggpht.com/-20qyx-3jGbk/AAAAAAAAAAI/AAAAAAAAAAA/Cd4GMXi7FbE/s88-c-k-no-mo-rj-c0xffffff/photo.jpg"

        imageContent = None
        try:
            imageContent = getHTTPS.getUrlContent(url)
        except:
            with open("image_placeholder.gif", 'rb') as imageFile:
                imageContent = imageFile.read()

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imageContent)
        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(pixmap)
        #imageLabel.setText("Test Text")
        self.vbox.addWidget(imageLabel)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def setBrowserPage(self):
        self.numClicks += 1
        if (not(self.browserPage is None)):
            self.vbox.removeWidget(self.browserPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.browserPage.setParent(None)

        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        # For general use, widgets should be added to scrollLayout below here,
        # but before browserPage has setWidget called.

        # Below is some test code
        clicksLabel = QtWidgets.QLabel("Number of Clicks: " + str(self.numClicks))
        scrollLayout.addWidget(clicksLabel)
        labelString = ""
        for i in range(1, 30):
            labelString += "Test " + str(i) + " "
        #l = QtWidgets.QLabel(labelString)
        l = ResizeLabel(self, labelString, self.resized)
        l.setWordWrap(True)
        l.setFixedWidth(self.width() - 50)
        scrollLayout.addWidget(l)

        self.browserPage = QtWidgets.QScrollArea()
        self.browserPage.setWidget(pageWidget)
        self.vbox.addWidget(self.browserPage)

    def linkClicked(self, urlString):
        print("Chosen Link: " + urlString)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(QtWidgets.QWidget(self))

    def printWidgetMargins(self, widget):
        left, top, right, bottom = widget.getContentsMargins()
        print(left)
        print(top)
        print(right)
        print(bottom)

class RenderImage():

    def __init__(self):
        pass

    def getWidget(self, url):
        c = ssl._create_unverified_context()
        img = urllib.request.urlopen(url, context=c)
        pixmap = QPixmap()
        pixmap.loadFromData(img.read())
        return pixmap

class ResizeLabel(QtWidgets.QLabel):

    def __init__(self, mainWindow, labelText, resizedSignal):
        super().__init__(labelText)
        self.mainWindow = mainWindow
        resizedSignal.connect(self.foo)

    def foo(self):
        self.setFixedWidth(self.mainWindow.width() - 50)
        self.repaint(0, 0, self.width(), self.height())

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BrowserWindow()
    sys.exit(app.exec_())
"""

if __name__ == "__main__":
    browserApplication = QtWidgets.QApplication(sys.argv)
    browserWindow = BrowserWindow()
    sys.exit(browserApplication.exec_())
'''
