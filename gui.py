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

    def __init__(self, browser):
        super(window, self).__init__()
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 300
        self.setGeometry(100,100,1000,600)
        #self.setMinimumSize(QSize(1000,600))
        self.setWindowTitle("Foxtrot Browser")

        #menu bar
        # mainMenu = self.menuBar()
        #
        # historyAction = QAction('&View History', self)
        # historyAction.setShortcut('Ctrl+H')
        # historyAction.triggered.connect(lambda:self.showHistory())
        #
        # clearHistoryAction = QAction('&Clear History', self)
        # clearHistoryAction.triggered.connect(lambda:self.clearHistory())
        #
        # sourceCodeAction = QAction('&View Source Code', self)
        # sourceCodeAction.triggered.connect(lambda:self.sourcePage())
        #
        # self.FileMenu = mainMenu.addMenu('&File')
        # self.FileMenu.addAction(self.sourceCodeAction)
        # self.FileMenu.addAction(self.historyAction)
        # self.FileMenu.addAction(self.clearHistoryAction)

        self.browser = browser

        self.table_widget = MyView(self,browser)
        self.setCentralWidget(self.table_widget)

        #self.table_widget = MyTabBar(self, strList)
        #self.setCentralWidget(self.table_widget)
        self.show()

    #Menu default action for nonfuncitional task
    def close_application(self):
        print('You pressed the action and closed the window')
        sys.exit()

class MyView(QWidget):

    def __init__(self, parent,browser):
        super(QWidget, self).__init__()
        self.browser = browser

        #Create Buttons:

        #Back Button
        self.backButton = QPushButton("<")
        self.backButton.clicked.connect(lambda:self.showBack())

        #Forward Button
        self.forwardButton = QPushButton(">")
        self.forwardButton.clicked.connect(lambda:self.showForward())

        #Refresh Button
        refreshButton = QPushButton()
        refreshButton.clicked.connect(lambda:self.prototype_loadWebpage(browser.currentPageUrl))
        refreshButton.setIcon(QtGui.QIcon('refresh.png'))

        #home Button
        homepageButton = QPushButton()
        homepageButton.clicked.connect(lambda:self.showHome())
        homepageButton.setIcon(QtGui.QIcon('home.png'))

        # URL Text Bar
        urlBar = QLabel()
        urlBar.setText('URL')
        self.bar = QLineEdit()

        #URL Bar Search Button
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(lambda:self.prototype_loadWebpage(self.bar.text()))
        searchButton.setShortcut("Return")

        #Create first roll which is a horizontal layout
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()

        #add widgets on the first roll of the vboxlayout
        hbox1.addWidget(self.backButton)
        hbox1.addWidget(self.forwardButton)
        hbox1.addWidget(refreshButton)
        hbox1.addWidget(homepageButton)
        hbox1.addWidget(urlBar)
        hbox1.addWidget(self.bar)
        hbox1.addWidget(searchButton)

        #Create veritcal layout
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox1)
        self.vbox2 = QVBoxLayout()
        self.vbox3 = QVBoxLayout()

        #Create buttons for second role
        sourceCodeButton = QPushButton("Source Code")
        sourceCodeButton.clicked.connect(lambda:self.sourcePage())
        historyButton = QPushButton("History")
        historyButton.clicked.connect(lambda:self.showHistory())
        clearHistoryButton = QPushButton("Clear History")
        clearHistoryButton.clicked.connect(lambda:self.clearHistory())

        favoriteButton = QPushButton("Favorites")
        favoriteButton.clicked.connect(lambda:self.showFavs())
        addFavoriteButton = QPushButton("Favorite Current Page")
        addFavoriteButton.clicked.connect(lambda:self.browser.addFavorite())
        setHomeButton = QPushButton("Set Home")
        setHomeButton.clicked.connect(lambda:self.browser.setHome())
        self.tabButton = QPushButton("New tab")
        self.tabButton.clicked.connect(self.addNewTab)

        hbox2.addWidget(self.tabButton)

        hbox2.addWidget(sourceCodeButton)
        hbox2.addWidget(historyButton)
        hbox2.addWidget(clearHistoryButton)
        hbox2.addWidget(favoriteButton)
        hbox2.addWidget(addFavoriteButton)
        hbox2.addWidget(setHomeButton)
        self.vbox.addLayout(hbox2)


        self.setLayout(self.vbox)
        self.currentPage = None

        #tab section
        self.i = 0
        self.listWidget = QListWidget(self)
        #self.deleteListWidget = QListWidget(self)

        #actions for tabs
        self.listWidget.itemClicked.connect(self.quickyTab)

        #self.deleteListWidget.itemClicked.connect(self.quickyTab)
        #self.listWidget.itemClicked.connect(self.buildExamplePopup())
        #self.listWidget.itemDoubleClicked.connect())

        #self.button = QPushButton("Add tab")
        #self.button.clicked.connect(self.addNewTab)
        
        '''
        for x in range(0, 10):
            okay = QListWidgetItem("X")
            self.deleteListWidget.addItem(okay)
        '''

        item = QListWidgetItem(self.browser.getLabelForTabs())
        self.listWidget.addItem(item)

        #self.hbox4.addWidget(self.deleteListWidget)
        self.hbox4.addWidget(self.listWidget)

        self.wid1 = QWidget()
        self.wid1.setLayout(self.hbox4)
        self.wid1.setFixedWidth(150)
        self.hbox3.addWidget(self.wid1)#10

        self.change = QPushButton("<")
        self.change.clicked.connect(self.doAnim)
        self.vbox3.addWidget(self.change)
        wid2 = QWidget()
        wid2.setLayout(self.vbox3)
        wid2.setFixedWidth(30)
        self.hbox3.addWidget(wid2)#1


        self.vbox.addLayout(self.hbox3)

        # The browser's current homepage
        firstpage = browser.loadHome()
        self.prototype_loadWebpage(firstpage)

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
                    for child in renderObject.widget.children():
                        if (not(isinstance(child, QtWidgets.QBoxLayout))):
                            child.linkActivated.connect(self.prototype_loadWebpage)
                    #renderObject.widget.linkActivated.connect(self.prototype_loadWebpage)
                scrollLayout.addWidget(renderObject.widget)

        self.listWidget.item(self.browser.currentTabIndex).setText(self.removeHTTPS(self.browser.currentPageUrl))
        self.browser.updateCurrentTag()

        self.currentPage = QtWidgets.QScrollArea()
        self.currentPage.setWidget(pageWidget)
        self.hbox3.addWidget(self.currentPage,100)
        self.updateEnabledNavigationButtons()
        #Could not figure out how to change a hboxlayout to weight 0, so I am
        #changing the wiget within the layout hide the tab bar.

    def loadNewTab(self, url):
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
                    for child in renderObject.widget.children():
                        if (not(isinstance(child, QtWidgets.QBoxLayout))):
                            child.linkActivated.connect(self.prototype_loadWebpage)
                #renderObject.widget.linkActivated.connect(self.prototype_loadWebpage)
                scrollLayout.addWidget(renderObject.widget)

        self.currentPage = QtWidgets.QScrollArea()
        self.currentPage.setWidget(pageWidget)
        self.hbox3.addWidget(self.currentPage,80)


    def doAnim(self):
        if(self.wid1.width()!=0):
            self.change.setText(">")
            self.wid1.setFixedWidth(0)
        else:
            self.wid1.setFixedWidth(200)
            self.change.setText("<")

#        self.anim = QPropertyAnimation(self.wid1, b"geometry")
#        self.anim.setDuration(300)
#        self.anim.setEndValue(self.wid1.setFixedWidth(200))
#        self.anim.start()

    #impliment later
    def quickyTab(self, item):
        index = self.listWidget.currentRow()
        print(str(index))
        # self.quickLoad(self.browser.getSiteFromTabs(index))
        self.browser.currentTabIndex = index
        self.prototype_loadWebpage(self.browser.getSiteFromTabs(index))
        return
        
    '''
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
    '''

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
        self.hbox3.addWidget(self.currentPage,80)

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
            label.linkActivated.connect(self.prototype_loadWebpage)
            scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.hbox3.addWidget(self.currentPage,80)

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

        for renderText in self.browser.showFavorites():
            label = QLabel(renderText)
            label.linkActivated.connect(self.prototype_loadWebpage)
            scrollLayout.addWidget(label)

        self.currentPage.setWidget(pageWidget)
        self.hbox3.addWidget(self.currentPage,80)

    def clearHistory(self):
        self.browser.clearHistory()
        self.updateEnabledNavigationButtons()
        self.showHistory()

    def showBack(self):
        url = self.browser.navigateBack()
        self.prototype_loadWebpage(url)
        self.backButton.setEnabled(self.canGoBack())

    def showForward(self):
        url = self.browser.navigateForward()
        self.prototype_loadWebpage(url)
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
        self.loadNewTab(self.browser.loadHome()) #load the homepage for the new tab
        self.browser.openNewTab()
        label = self.browser.getLabelForTabs()
        newItem = QListWidgetItem(self.removeHTTPS(label))
        self.listWidget.addItem(newItem)
    
    

    '''
       removes the https:// and the .com, .edu, .gov from urls
       used for labeling tabs
    '''
    def removeHTTPS(self, url):
        if url[8:12] == "www.":
            temp = url[12:(len(url) - 4)]
        else:
            temp = url[8:(len(url) - 4)]
        return temp
'''
class ExamplePopup(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)
'''

def main(browser):
    app = QApplication(sys.argv)
    Gui = window(browser)
    sys.exit(app.exec_())

if __name__ == '__main__':
    browser = FoxBrowser()
    main(browser)
