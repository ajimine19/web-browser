#import unittest
import os
import sys
sys.path.append(os.path.abspath("web-browser-sq2018-foxtrottt"))
from FoxBrowser import *

def test_addToTabs():
    fb = FoxBrowser()
    fb.tabSites = ["webpage1", "webpage2"]
    fb.addToTabs("webpage3")
    assert (len(fb.tabSites)==3)

def test_addToTabsNone():
    fb = FoxBrowser()
    fb.tabSites = ["webpage1", "webpage2"]
    fb.addToTabs(None)
    assert (len(fb.tabSites)==2)

def test_getSiteFromTabs():
    fb = FoxBrowser()
    fb.tabSites = ["webpage1","webpage2","webpage3"]
    page1 = fb.getSiteFromTabs(0)
    assert(page1 == "webpage1")


    
