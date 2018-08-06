
import csv
import os
import sys
sys.path.append(os.path.abspath(""))
from NavigationHistory import NavigationHistory

def test_moveBack():
    myHist = NavigationHistory("test_history.csv")
    myHist.history = ["site1", "site2", "site3"] #manual history to control test
    #test that it returns the previous site
    assert myHist.moveBack() == "site2"
    assert myHist.historyPageIndex == 1
    # test that if can't move back, it stays on same webpage
    myHist.historyPageIndex = 2
    assert myHist.moveBack() is None

def test_moveForward():
    myHist = NavigationHistory("test_history.csv")
    myHist.history = ["site1", "site2", "site3"] #manual history to control test
    #test that if it can't move forward, it stays on same webpage
    assert myHist.moveForward() is None
    #test that it moves forward
    myHist.historyPageIndex = 2
    assert myHist.moveForward() == "site2"
    assert myHist.historyPageIndex == 1

def test_addToHist():
    temp = []
    url = "testURL"
    myHist = NavigationHistory("test_history.csv")
    myHist.history = ["site1", "site2", "site3"] #manual history to control test
    myHist.addToHist(url)
    assert "".join(myHist.history[0]) == "testURL"

def test_clear():
    myHist = NavigationHistory("test_history.csv")
    myHist.clearHist()
    assert len(myHist.history) == 1 #should only have current page in the file now
