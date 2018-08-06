import csv
"""
    This class is responsible for keeping track of the user's
    current browsing history.
"""

class NavigationHistory:

    """
        Constructor
        initialize variables
        args
        -filename: give a file to store the history to
        """
    def __init__(self, filename):
        self.historyPageIndex = 0
        self.history = []
        self.historyfile = filename
        self.updateHistory()
    """
        updateHistory
        reads the history file to update the current browser history
        """
    def updateHistory(self):
        self.history = []
        with open(self.historyfile, 'r', newline = '\n') as file:
            temp = csv.reader(file)
            for page in temp:
                self.history = [page] + self.history

    """
        moveBack
        if able to move back, it return the page url to load
        """
    def moveBack(self):
        if(self.historyPageIndex < len(self.history) -1): #check if there is a page to go back to
            self.historyPageIndex += 1 #increment the index
            return "".join(self.history[self.historyPageIndex]) #return the new page to load
        else:
            print("No webpage to go back to") # for error handling/debugging
            return None

    """
        moveForward
        if able to move forward, it returns the page url to load
        """
    def moveForward(self):
        if(self.historyPageIndex > 0): #make sure there is a page to go forward to
            self.historyPageIndex -= 1 #decrement the index
            return "".join(self.history[self.historyPageIndex]) #return the new page to load
        else:
            print("No webpage to go forward to") # for error handling/debugging
            return None


    def printHistory2(self): #prints the history to terminal / mainly for debugging
        print("\n-----HISTORY-----\n")
        for page in range(len(self.history)):
            print(str(page+1) + ")" + "".join(self.history[page]) + "\n")

    """
        printHistory
        converts the current history to have link tags
        """
    def printHistory(self):
        histList = []
        tag1 = '<a href="'
        tag2 = '">'
        tag3 = '<\\a>'
        for page in range(len(self.history)):
            histList.append((tag1 + "".join(self.history[page]) + tag2 + "".join(self.history[page]) + tag3))
        return histList

    """
        clearHist
        empty the history file and current array and writes the current page to it
        """
    def clearHist(self): # 'clear' the csv file
        currentPage = "".join(self.history[self.historyPageIndex])
        histFile = open(self.historyfile, 'w')
        writer = csv.writer(histFile, delimiter = ',')
        writer.writerows([currentPage.split(',')])
        histFile.close()
        self.updateHistory()

    """
        addToHist
        appends the new url to the history file and to the front of the current working history
        only adds to history if we are not already navigating through the history
        args
        -url: the url being added
        """
    def addToHist(self, url): #used in loadWebpage
        #only add if we are not navigating forward/backward
        if(self.historyPageIndex == 0 and "".join(self.history[self.historyPageIndex]) != url):
            histFile = open(self.historyfile, 'a')
            writer = csv.writer(histFile, delimiter = ',')
            writer.writerows([url.split(',')])
            histFile.close()
            self.updateHistory()#appends to the front of list
        return
        #future work: if url already exists in the file, remove it and put at front

if __name__ == "__main__":
    h = NavigationHistory("history.csv")
