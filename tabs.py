import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton, QWidget, QListWidget, QListWidgetItem, QLabel, QApplication, QDialog, QVBoxLayout


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.i = 0
        self.listWidget = QListWidget(self)

        self.listWidget.itemClicked.connect(self.buildExamplePopup)
        #self.listWidget.itemDoubleClicked.connect())

        self.button = QPushButton("Add tab")
        self.button.clicked.connect(self.addNewTab)



        tab = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"]
        for n in tab:
            self.i = self.i+1
            item = QListWidgetItem("Tab %d" %self.i)
            self.listWidget.addItem(item)
            #set icon
        self.setGeometry(300, 300, 300, 300)
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addWidget(self.listWidget)
        self.setLayout(vbox)
        self.show()

    @pyqtSlot(QListWidgetItem)
    def buildExamplePopup(self, item):
        exPopup = ExamplePopup(item.text(), self)
        exPopup.setGeometry(50, 400, 100, 100)
        exPopup.show()

    def addNewTab(self):
        self.i = self.i + 1
        newItem = QListWidgetItem("Tab %d"%self.i)
        self.listWidget.addItem(newItem)

class ExamplePopup(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)
########################
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox1)
        self.vbox2 = QVBoxLayout()

        #Create buttons for second role
        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(lambda:self.prototype_loadWebpage(browser.currentPageUrl))
        sourceCodeButton = QPushButton("Source Code")
        sourceCodeButton.clicked.connect(lambda:self.sourcePage())
        historyButton = QPushButton("History")
        historyButton.clicked.connect(lambda:self.showHistory())
        clearHistoryButton = QPushButton("Clear History")
        clearHistoryButton.clicked.connect(lambda:self.clearHistory())
        favoriteButton = QPushButton("Favorites")
        favoriteButton.clicked.connect(lambda:self.showFavs())
        clearfavoriteButton = QPushButton("Favorite Current Page")
        clearfavoriteButton.clicked.connect(lambda:self.browser.addFavorite())
        # homepageButton = QPushButton("Homepage")
        # homepageButton.clicked.connect(lambda:self.showHome())
        # setHomeButton = QPushButton("Set Home")
        # setHomeButton.clicked.connect(lambda:self.browser.setHome())


        hbox2.addWidget(refreshButton)
        hbox2.addWidget(sourceCodeButton)
        hbox2.addWidget(historyButton)
        hbox2.addWidget(clearHistoryButton)
        hbox2.addWidget(favoriteButton)
        hbox2.addWidget(clearfavoriteButton)
        # hbox2.addWidget(homepageButton)
        # hbox2.addWidget(setHomeButton)
        self.vbox.addLayout(hbox2)

        self.setLayout(self.vbox)
        self.currentPage = None

        #tab section
        self.i = 0
        self.listWidget = QListWidget(self)

        self.listWidget.itemClicked.connect(self.buildExamplePopup)
        #self.listWidget.itemDoubleClicked.connect())

        self.button = QPushButton("Add tab")
        self.button.clicked.connect(self.addNewTab)

        tab = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"]
        for n in tab:
            self.i = self.i+1
            item = QListWidgetItem("Tab %d" %self.i)
            self.listWidget.addItem(item)
            #set icon
        self.setGeometry(300, 300, 300, 300)
        self.vbox2.addWidget(self.button)
        self.vbox2.addWidget(self.listWidget)
        self.hbox3.addLayout(self.vbox2)
        # The browser's current homepage
        self.loadWebpage(self.browser.homepage)
        self.vbox.addLayout(self.hbox3)
#######################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExampleWidget()
    ex.show()
    sys.exit(app.exec_())


==================
import sys
import os
import ssl
import re
import urllib.request
import time
import RenderObject
sys.path.append(os.path.abspath("Tokenizer"))
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from HTMLTokenizer import *
from FoxBrowser import *

##################
# Created a window class and a tab class
# Window class creates the display canvas
# Tab class creates thsofe tab pages
# Used QGridLayout layout
#http://doc.qt.io/qt-5/qscrollarea.html
##################


class window(QMainWindow):

    def __init__(self,strList, browser):
        super(window, self).__init__()
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 300
        self.setGeometry(100,100,1000,600)
        #self.setMinimumSize(QSize(1000,600))
        self.setWindowTitle("Foxtrot Browser")


        #Create seperate clas for menu bar
        extractAction = QAction('&File Action', self)
        extractAction.setShortcut('Ctrl+A')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)

        historyAction = QAction('&history Action', self)
        historyAction.setShortcut('Ctrl+H')
        historyAction.setStatusTip('Activate the history')
        historyAction.triggered.connect(self.close_application)

        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        tabMenu = mainMenu.addMenu('&History')
        tabMenu.addAction(historyAction)

        self.browser = browser

        self.table_widget = MyView(self, strList,browser)
        self.setCentralWidget(self.table_widget)

        #self.table_widget = MyTabBar(self, strList)
        #self.setCentralWidget(self.table_widget)
        self.show()

    #Menu default action for nonfuncitional task
    def close_application(self):
        print('You pressed the action and closed the window')
        sys.exit()

class MyView(QWidget):

    def __init__(self, parent, strList,browser):
        super(QWidget, self).__init__()
        self.browser = browser
        strList = '\n'.join(strList)
        c = ssl._create_unverified_context()
        img = urllib.request.urlopen("https://i.ytimg.com/vi/n8us60ow3iM/maxresdefault.jpg", context=c)
        imgContent = img.read()

        #Create Buttons:

        #Back Button
        self.backButton = QPushButton("<")
        self.backButton.clicked.connect(lambda:self.showBack())

        #Forward Button
        self.forwardButton = QPushButton(">")
        self.forwardButton.clicked.connect(lambda:self.showForward())

        # URL Text Bar
        urlBar = QLabel()
        urlBar.setText('URL')
        self.bar = QLineEdit()

        #URL Bar Search Button
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(lambda:self.prototype_loadWebpage(self.bar.text()))
        searchButton.setShortcut("Return")

        #Create horizontal layout
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        #add widgets:
        hbox1.addWidget(self.backButton)
        hbox1.addWidget(self.forwardButton)
        hbox1.addWidget(urlBar)
        hbox1.addWidget(self.bar)
        hbox1.addWidget(searchButton)

        #Create veritcal layout
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox1)
        self.vbox2 = QVBoxLayout()


        #Create buttons for second role
        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(lambda:self.prototype_loadWebpage(browser.currentPageUrl))
        sourceCodeButton = QPushButton("Source Code")
        sourceCodeButton.clicked.connect(lambda:self.sourcePage())
        historyButton = QPushButton("History")
        historyButton.clicked.connect(lambda:self.showHistory())
        clearHistoryButton = QPushButton("Clear History")
        clearHistoryButton.clicked.connect(lambda:self.clearHistory())
        favoriteButton = QPushButton("Favorites")
        favoriteButton.clicked.connect(lambda:self.showFavs())
        clearfavoriteButton = QPushButton("Favorite Current Page")
        clearfavoriteButton.clicked.connect(lambda:self.browser.addFavorite())
        homepageButton = QPushButton("Homepage")
        homepageButton.clicked.connect(lambda:self.showHome())
        setHomeButton = QPushButton("Set Home")
        setHomeButton.clicked.connect(lambda:self.browser.setHome())


        hbox2.addWidget(refreshButton)
        hbox2.addWidget(sourceCodeButton)
        hbox2.addWidget(historyButton)
        hbox2.addWidget(clearHistoryButton)
        hbox2.addWidget(favoriteButton)
        hbox2.addWidget(clearfavoriteButton)
        hbox2.addWidget(homepageButton)
        hbox2.addWidget(setHomeButton)
        self.vbox.addLayout(hbox2)

        self.setLayout(self.vbox)
        self.currentPage = None

        #tab section
        self.i = 0
        self.listWidget = QListWidget(self)

        self.listWidget.itemClicked.connect(self.buildExamplePopup)
        #self.listWidget.itemDoubleClicked.connect())

        self.button = QPushButton("Add tab")
        self.button.clicked.connect(self.addNewTab)

        tab = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"]
        for n in tab:
            self.i = self.i+1
            item = QListWidgetItem("Tab %d" %self.i)
            self.listWidget.addItem(item)
            #set icon
        self.setGeometry(300, 300, 300, 300)
        self.vbox2.addWidget(self.button)
        self.vbox2.addWidget(self.listWidget)
        self.hbox3.addLayout(self.vbox2)
        # The browser's current homepage
        self.prototype_loadWebpage("faculty.up.edu/oster")
        self.vbox.addLayout(self.hbox3)

        # The browser's current homepage
<<<<<<< HEAD
        #self.prototype_loadWebpage("https://theuserisdrunk.com")

        #self.prototype_loadWebpage("www.google.com")
=======
        firstpage = browser.loadHome()
        self.prototype_loadWebpage(firstpage)
>>>>>>> c339c585f442a4226fe323491224d96914b166ad

    def prototype_loadWebpage(self, url):
        # Free the widget containing the current webpage
        if (not(self.currentPage is None)):
            self.vbox.removeWidget(self.currentPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.currentPage.setParent(None)

        if (not(self.urlStartsWithHTTPS(url))):
            url = "https://" + url
        self.bar.setText(url)
        renderObjectList = self.browser.prototype_loadWebpage(url)

        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        if (not(renderObjectList is None)):
            for renderObject in renderObjectList:
                #renderObject.printObjectInfo()
                if (renderObject.objectType == RenderObject.ObjectType.Hyperlink):
                    renderObject.widget.linkActivated.connect(self.prototype_loadWebpage)
                scrollLayout.addWidget(renderObject.widget)

        self.currentPage = QtWidgets.QScrollArea()
        self.currentPage.setWidget(pageWidget)
        self.hbox3.addWidget(self.currentPage)

    def loadWebpage(self, url):
        if (not(self.urlStartsWithHTTPS(url))):
            url = "https://" + url
        self.bar.setText(url)
        self.browser.submitPageUrl(url)
        start_time = time.time()
        # Remove the current browser page widgets
        if (not(self.currentPage is None)):
            self.vbox.removeWidget(self.currentPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.currentPage.setParent(None)

        self.currentPage = QtWidgets.QScrollArea()
        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        #Added to show we can print a photo
#        c = ssl._create_unverified_context()
#        img = urllib.request.urlopen("https://i.ytimg.com/vi/n8us60ow3iM/maxresdefault.jpg", context=c)
#        imgContent = img.read()
#        #Print out picture label
#        label1 = QLabel(self)
#        pixmap = QPixmap()
#        pixmap.loadFromData(imgContent)
#        pixmap2 = pixmap.scaled(1000, 1500, Qt.KeepAspectRatio)
#        label1.setPixmap(pixmap2)
#        label1.setAlignment(Qt.AlignCenter)
#        scrollLayout.addWidget(label1)

        #Changes background color if their is a string hex inside the token list
        for renderText in self.browser.htmlTokenizer.getRenderList():
            if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', renderText):
                self.setStyleSheet("background-color:" + renderText + ";")
            else:
                label = QLabel(renderText)
                label.linkActivated.connect(self.loadWebpage)
                scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.vbox.addWidget(self.currentPage)
        print("--- %s seconds ---" % (time.time() - start_time))

        self.updateEnabledNavigationButtons()

    def urlStartsWithHTTPS(self, url):
        if (len(url) < 4):
            return False
        return (url[0:4] == "http")

    def sourcePage(self):
         # Remove the current browser page widgets
        if (not(self.currentPage is None)):
            self.vbox.removeWidget(self.currentPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.currentPage.setParent(None)

        self.currentPage = QtWidgets.QScrollArea()
        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        sourceCode = self.browser.showDeveloperSourceCode()

        label = QPlainTextEdit(sourceCode)
        scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.vbox.addWidget(self.currentPage)

    def showHistory(self):
    # Remove the current browser page widgets
        if (not(self.currentPage is None)):
            self.vbox.removeWidget(self.currentPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.currentPage.setParent(None)

        self.currentPage = QtWidgets.QScrollArea()
        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        #iterates through the list of strings (websites) that is returned
        #from Adrian's history method called showHistory
        for renderText in self.browser.showHistory():
            label = QLabel(renderText)
            label.linkActivated.connect(self.loadWebpage)
            scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.vbox.addWidget(self.currentPage)

    def showFavs(self):
    # Remove the current browser page widgets
        if (not(self.currentPage is None)):
            self.vbox.removeWidget(self.currentPage)
            # VERY IMPORTANT : MEMORY LEAKS OCCUR WITHOUT setParent(None)
            self.currentPage.setParent(None)

        self.currentPage = QtWidgets.QScrollArea()
        scrollLayout = QtWidgets.QVBoxLayout()
        pageWidget = QtWidgets.QWidget()
        pageWidget.setLayout(scrollLayout)

        sourceCode = self.browser.showDeveloperSourceCode()

        hedd = ["hfjkds","fksjdhf"]
        for renderText in self.browser.showFavorites():
            label = QLabel(renderText)
            label.linkActivated.connect(self.loadWebpage)
            scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.vbox.addWidget(self.currentPage)

    def clearHistory(self):
        self.browser.clearHistory()
        self.updateEnabledNavigationButtons()

    def showBack(self):
        url = self.browser.navigateBack()
        self.loadWebpage(url)
        self.backButton.setEnabled(self.canGoBack())

    def showForward(self):
        url = self.browser.navigateForward()
        self.loadWebpage(url)
        self.forwardButton.setEnabled(self.canGoForward())

    def canGoBack(self):
        previousUrl = self.browser.navigateBack()
        previousPageExists = True
        if (previousUrl is None):
            previousPageExists = False
        else:
            self.browser.navigateForward()
        return previousPageExists

    def canGoForward(self):
        nextUrl = self.browser.navigateForward()
        nextPageExists = True
        if (nextUrl is None):
            nextPageExists = False
        else:
            self.browser.navigateBack()
        return nextPageExists

    def updateEnabledNavigationButtons(self):
        self.backButton.setEnabled(self.canGoBack())
        self.forwardButton.setEnabled(self.canGoForward())

    def style(self,renderText,font,fontSize):
        CSSUpdatelabel = Qlabel(renderText)
        newFont = QtGui.QFont("""font""",fontSize)
        self.CSSUpdatelabel.setFont(newFont)

    def showHome(self):
        url = self.browser.loadHome()
        self.prototype_loadWebpage(url)

    @pyqtSlot(QListWidgetItem)
    def buildExamplePopup(self, item):
        exPopup = ExamplePopup(item.text(), self)
        exPopup.setGeometry(50, 400, 100, 100)
        exPopup.show()

    def addNewTab(self):
        self.i = self.i + 1
        newItem = QListWidgetItem("Tab %d"%self.i)
        self.listWidget.addItem(newItem)

class ExamplePopup(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)
#Tab functionality for later
class MyTabBar(QWidget):

    def __init__(self, parent, strList):
        super(QWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(800,200)

        # Add tabs: add below but also intialize above...
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        self.tabs.addTab(self.tab3,"Tab 3")
        self.tabs.addTab(self.tab4,"Tab 4")

        # Create first tab
        self.tab1.layout = QGridLayout(self)

        #text
        strList = '\n'.join(strList)


        self.testDisplay1 = QLabel(self)
        self.testDisplay1.setText(strList)
        self.tab1.layout.addWidget(self.testDisplay1)

        self.pushButton1 = QPushButton("Action button")
        self.pushButton1.clicked.connect(QCoreApplication.instance().quit)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


def main(strList,browser):
    app = QApplication(sys.argv)
    Gui = window(strList, browser)
    sys.exit(app.exec_())

if __name__ == '__main__':
    strList = ["Sample text", "More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello",
               "\n \n \n \n More sample text \n \n \n \n hello"]

    browser = FoxBrowser()
    main(strList, browser)
