"""
    FoxBrowser

    This is the main entrypoint of our program and the main container of
    all program components.
"""

import csv
import PageLoader
from HTMLTokenizer import HTMLTokenizer
from getHTTPS import getHTML
from simpleCache import *
from NavigationHistory import NavigationHistory
from SaveFavorites import SaveFavorites
import time

class FoxBrowser:

    def __init__(self):
        # TODO: create a start page and initialize the history to contain that page

        self.navHist = NavigationHistory("history.csv")
        self.saveFav = SaveFavorites()
        self.currentPageUrl = self.readHome()
        self.currentPageSourceHTML = ""
        self.currentPageRenderObjects = []
        self.myCache = simpleCache()
        self.myCache.max_cache_size = 0
        self.tabSites = []
        self.tabRenderObjects = [] #parsed objects for quick loading between tabs
        self.currentTabIndex = 0
        self.totalTabs = 0
        self.tabSites.append(self.readHome())
        self.homeurl = self.readHome()

#------------------TAB FUNCTIONS------------------------#

    def addToTabs(self, url):
        if(url == None):
            pass
        else:
            self.tabSites.append(url)

    #this function should be called everytime a new tab is created, it should add the homepage as the new tab
    def openNewTab(self):
        self.tabSites.append(self.homeurl) #make the new tab open to the homepage
        self.tabRenderObjects.append(self.currentPageRenderObjects)
        self.currentTabIndex = self.totalTabs + 1 #the current tab should be the newly opened one
        self.totalTabs += 1 #increment the total tabs
        return
    
    # the function for getting the label for the tag
    def getLabelForTabs(self):
        return "".join(self.tabSites[self.currentTabIndex])

    #when a tab is clicked return the render objects to display the page on the gui, needs the index of the tab to be passed in
    def getSiteFromTabs(self, index):
    #return self.tabRenderObjects[index]
        return self.tabSites[index]
    
    #this function should get called everytime a new page is loaded while on a tag to update its information
    def updateCurrentTag(self):
        self.tabSites[self.currentTabIndex] = self.currentPageUrl
        #self.tabRenderObjects[self.currentTabIndex] = self.currentPageRenderObjects
        return
    
    '''
    def deleteTab(self, index):
        self.totalTabs -= 1
        tempList = [] #make a new list that includes urls in tabSites except the deleted one
        for x in range(len(self.tabSites)):
            if x != index:
                tempList.append(self.tabSites[x])
        self.tabSites = tempList
        tempList = [] #make a new list that includes the renderObjects except the deleted one
        for y in range(len(self.tabRenderObjects)):
            if y != index:
                tempList.append(self.tabRenderObjects[y])
        self.tabRenderObjects = tempList
        if index > 0:
            self.currentTabIndex = index -1 #revert back to the previous tab
        else:
            self.currentTabIndex = index +1 #go to the next tab
        return self.tabRenderObjects[self.currentTabIndex] #return the render objects to load the tab with quickLoad
    '''

#---------------------------------------------------------#

    def prototype_loadWebpage(self, url):
        start_time = time.time()
        pageLoader = PageLoader.PageLoader()
        loadResult = pageLoader.loadWebpage(url)
        self.currentPageSourceHTML = pageLoader.mySourceCode
        print("--- %s seconds ---" % (time.time() - start_time))
        
        if(loadResult != None):
            self.currentPageUrl = url
            self.currentPageRenderObjects = loadResult
        self.navHist.addToHist(url)
        return loadResult

    def submitPageUrl(self, pageUrl):
        # interface method for the GUI code
        self.navHist.currentPageIndex = 0
        self.pageLoader(pageUrl)

    def refreshPage(self):
        # interface method for the GUI code
        print("Refreshing Current Webpage")
        self.pageLoader(self.currentPageUrl)
        return self.currentStrList

    def showDeveloperSourceCode(self):
        # interface method for the GUI code
        return self.currentPageSourceHTML

    def navigateForward(self):
        return self.navHist.moveForward()

    def navigateBack(self):
        return self.navHist.moveBack()

    def clearHistory(self): #clear the text file
        self.navHist.clearHist()

    def showHistory(self): #pass the history to the gui
        return self.navHist.printHistory()

    def showFavorites(self):
        return self.saveFav.printFavorites()

    def addFavorite(self):
            url = self.currentPageUrl
            self.saveFav.addNewFavorite(url)

#--------------HOME PAGE FUNCTIONS------------------------#

    def setHome(self):
        with open("homepage.csv", "w") as file:
            file.write(self.currentPageUrl)
        self.homeurl = "".join(self.currentPageUrl)
        print(str(self.currentPageUrl) + " has been set to the home page")
        return

    def readHome(self):
        with open("homepage.csv", "r") as file:
            url = file.readlines()
        return "".join(url)

    def loadHome(self):
        return self.homeurl #pass the url to the gui to call loadWebpage

#----------------------------------------------------------#
    '''
    def setCache(self, size):
        self.myCache.setCache(size)
        return
    
    
    def pageLoader(self, url):
        """
            This method is responsible for connecting to the web page
            indicated by the url parameter, retrieving that
            page's html code, processing the html, and displaying the
            page contents to the screen.
        """
        self.currentPageUrl = url
        source = ""

        """
        if (self.myCache.__contains__(url)):
            print("In Cache")
            pageContents = self.myCache.getElement(url)
            self.printListOfStrings(pageContents)
            self.navHist.addToHist(url)
        else:
        """
        try:
            try:
                source = getHTML(url).decode(encoding = 'UTF-8', errors = 'strict')
            except:
                source = getHTML(url).decode(encoding = 'windows-1252', errors = 'strict')
        except:
            print(url + " could not be loaded")

        if (len(source) > 0):
            self.currentPageRootUrl = self.extractRootUrl(url)
            self.htmlTokenizer.rootUrl = self.currentPageRootUrl
            self.currentPageSourceHTML = source
            self.htmlTokenizer.parseHTML(self.currentPageSourceHTML)
            self.printListOfStrings(self.htmlTokenizer.strList)
            #self.myCache.updateCache(url, self.htmlTokenizer.strList) #add the page to cache
            self.navHist.addToHist(url) #write to the history file
            print(self.currentPageUrl + " was loaded")
        else:
            self.currentPageSource = ""
    

    def extractRootUrl(self, url):
        i = 0;
        slashCount = 0
        rootString = ""
        while (i < len(url)):
            rootString += url[i]
            if (url[i] == '/'):
                slashCount += 1
                if (slashCount > 2): # The next slash after http://
                    break
            i += 1
        return rootString
    

    def printListOfStrings(self, strList):
        for s in strList:
            print(s)
    '''

if __name__ == "__main__":
    browser = FoxBrowser()
